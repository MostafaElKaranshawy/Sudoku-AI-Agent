import random
import copy

class SudokuSolverCSP:
    def __init__(self, puzzle):
        self.puzzle = puzzle  # 9x9 grid with 0 for empty cells
        self.variables = [(r, c) for r in range(9) for c in range(9)]  # 81 variables (positions)
        self.domains = self.set_domains()  # domain of each variable (initially from 1->9) if not assigned
        self.arcs = self.generate_arcs() # all arcs between variables
        self.steps_queue = []  # queue to store the steps of the solution
        self.solving = False

    def set_domains(self):
        domains = {}
        for r in range(9):
            for c in range(9):
                if self.puzzle[r][c] != 0:
                    domains[(r, c)] = {self.puzzle[r][c]}
                else:
                    domains[(r, c)] = set(range(1, 10))
        return domains

    def generate_arcs(self):
        # rows
        arcs = set()
        for r in range(9):
            for c1 in range(9):
                for c2 in range(c1 + 1, 9):
                    arcs.add(((r, c1), (r, c2)))
                    arcs.add(((r, c2), (r, c1)))

        # columns
        for c in range(9):
            for r1 in range(9):
                for r2 in range(r1 + 1, 9):
                    arcs.add(((r1, c), (r2, c)))
                    arcs.add(((r2, c), (r1, c)))

        # boxes
        for box_r in range(3):
            for box_c in range(3):
                cells = [(box_r * 3 + r, box_c * 3 + c) for r in range(3) for c in range(3)]
                for i in range(len(cells)):
                    for j in range(i + 1, len(cells)):
                        arcs.add((cells[i], cells[j]))
                        arcs.add((cells[j], cells[i]))

        return arcs

    def is_consistent(self, value, y):
        if value in self.domains[y]:
            return len(self.domains[y]) > 1
        return True


    # does the domain reduction if the value is not consistent
    def revise(self, x, y):
        revised = False
        for value in set(self.domains[x]):
            if not self.is_consistent(value, y):
                # Print the arcs before deletion
                if self.solving:
                    print(f"Before deletion:")
                    print(f"{x} -> {self.domains[x]}")
                    print(f"{y} -> {self.domains[y]}")
                    print(f"Inconsistent value being removed from {x}: {value}")

                self.domains[x].remove(value)
                revised = True

                if self.solving:
                    # Print the arcs after deletion
                    print(f"After deletion:")
                    print(f"{x} -> {self.domains[x]}")
                    print(f"{y} -> {self.domains[y]}")
                    print()

                if len(self.domains[x]) == 1:  # Domain reduced to a single value
                    # Add the variable and its fixed value to the queue
                    self.steps_queue.append((x, next(iter(self.domains[x]))))

        return revised


    def apply_arc_consistency(self):
        queue = list(self.arcs)
        while queue:
            x, y = queue.pop(0)
            if self.revise(x, y):
                if not self.domains[x]:
                    return False  # No solution exists

                for neighbor in self.get_neighbors(x):
                    if neighbor != y:
                        queue.append((neighbor, x))

        return True

    # get all neighbors of a cell (row, column, box)
    def get_neighbors(self, cell):
        r, c = cell
        neighbors = set()
        for i in range(9):
            if i != c:
                neighbors.add((r, i))
            if i != r:
                neighbors.add((i, c))
        box_r, box_c = r // 3, c // 3
        for i in range(box_r * 3, box_r * 3 + 3):
            for j in range(box_c * 3, box_c * 3 + 3):
                if (i, j) != cell:
                    neighbors.add((i, j))
        return neighbors


    def fill_puzzle(self):
        for position, domain in self.domains.items():
            self.puzzle[position[0]][position[1]] = next(iter(domain))

    def solve(self):
        if not self.apply_arc_consistency():
            return False

        result = self.backtrack()
        if result:
            self.fill_rest_of_steps()
            self.fill_puzzle()
            return True

        return False

    def backtrack(self):

        # solution found
        if all(len(self.domains[var]) == 1 for var in self.variables):
            return True

        if any(len(self.domains[var]) == 0 for var in self.variables):
            return False

        # Select unassigned variable with minimum remaining values
        unassigned_vars = [var for var in self.variables if len(self.domains[var]) > 1]
        var = min(unassigned_vars, key=lambda var: len(self.domains[var]))


        # Shuffle the values to be assigned to the variable to generate random solutions if multiple solutions exist
        to_be_shuffled_values = list(self.domains[var])
        random.shuffle(to_be_shuffled_values)

        # try assigning each value to the variable
        for value in to_be_shuffled_values:
            old_domains = copy.deepcopy(self.domains)
            old_steps_queue = copy.deepcopy(self.steps_queue)
            self.domains[var] = {value}  # (0, 2)
            if self.apply_arc_consistency():
                if self.backtrack():
                    return True

            self.domains = old_domains
            self.steps_queue = old_steps_queue
        return False

    def display_steps(self):
        print("Steps to solve the Sudoku:")
        for step in self.steps_queue:
            print(f"Set position {step[0]} to {step[1]}")

    def fill_rest_of_steps(self):
        steps_set = set()
        for i in range(len(self.steps_queue)):
            steps_set.add(self.steps_queue[i][0])

        for r in range(9):
            for c in range(9):
                if (r, c) not in steps_set and self.puzzle[r][c] == 0:
                    self.steps_queue.append(((r, c), next(iter(self.domains[(r, c)]))))
                    steps_set.add((r, c))

# Example usage
puzzle = [
    [7, 9, 0, 0, 1, 3, 6, 0, 0],
    [4, 0, 0, 0, 7, 0, 3, 0, 0],
    [1, 0, 0, 2, 4, 0, 9, 7, 5],
    [5, 0, 0, 6, 0, 0, 2, 0, 7],
    [0, 7, 0, 0, 0, 1, 8, 0, 0],
    [8, 0, 6, 9, 2, 0, 5, 0, 0],
    [6, 0, 1, 0, 0, 2, 0, 5, 3],
    [3, 0, 0, 0, 0, 0, 4, 0, 9],
    [0, 2, 4, 0, 3, 5, 0, 0, 0]
]
