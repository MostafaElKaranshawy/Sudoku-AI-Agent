import random
import copy

class SudokuSolverCSP:
    def __init__(self, puzzle):
        self.puzzle = puzzle  # 9x9 grid with 0 for empty cells
        self.variables = [(r, c) for r in range(9) for c in range(9)]
        self.domains = self.initialize_domains()
        self.constraints = self.generate_constraints()

    def initialize_domains(self):
        """Initialize domains for all cells."""
        domains = {}
        for r in range(9):
            for c in range(9):
                if self.puzzle[r][c] != 0:
                    domains[(r, c)] = {self.puzzle[r][c]}
                else:
                    domains[(r, c)] = set(range(1, 10))
        return domains

    def generate_constraints(self):
        """Generate arcs (constraints) for rows, columns, and subgrids."""
        # constraints = []
        constraints = set()
        for r in range(9):
            for c1 in range(9):
                for c2 in range(c1 + 1, 9):
                    constraints.add(((r, c1), (r, c2)))
                    constraints.add(((r, c2), (r, c1)))
        for c in range(9):
            for r1 in range(9):
                for r2 in range(r1 + 1, 9):
                    constraints.add(((r1, c), (r2, c)))
                    constraints.add(((r2, c), (r1, c)))

        for box_r in range(3):
            for box_c in range(3):
                cells = [(box_r * 3 + r, box_c * 3 + c) for r in range(3) for c in range(3)]
                for i in range(len(cells)):
                    for j in range(i + 1, len(cells)):
                        constraints.add((cells[i], cells[j]))
                        constraints.add((cells[j], cells[i]))

        return constraints

    def is_consistent(self, x, value, y):
        """Check if assigning value to x is consistent with y."""
        if value in self.domains[y]:
            return len(self.domains[y]) > 1
        return True


    # does the domain reduction
    def revise(self, x, y):
        """Revise the domain of x based on y, printing arcs before and after deletions."""
        revised = False
        for value in set(self.domains[x]):  # Use a copy of the domain to avoid issues while iterating
            if not self.is_consistent(x, value, y):
                # Print the arcs before deletion
                print(f"Before deletion:")
                print(f"{x} -> {self.domains[x]}")
                print(f"{y} -> {self.domains[y]}")
                print(f"Inconsistent value being removed from {x}: {value}")

                self.domains[x].remove(value)
                revised = True

                # Print the arcs after deletion
                print(f"After deletion:")
                print(f"{x} -> {self.domains[x]}")
                print(f"{y} -> {self.domains[y]}")
                print()
        return revised

    def apply_arc_consistency(self):
        """Enforce arc consistency for all arcs."""
        queue = list(self.constraints)
        while queue:
            x, y = queue.pop(0)
            if self.revise(x, y):
                if not self.domains[x]:
                    return False  # No solution exists

                for neighbor in self.get_neighbors(x):
                    if neighbor != y:
                        queue.append((neighbor, x))

        return True

    def get_neighbors(self, cell):
        """Get all neighbors of a cell."""
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

    def assign_singletons(self):
        """Assign values to cells with singleton domains."""
        for cell, domain in self.domains.items():
            if len(domain) == 1:
                self.puzzle[cell[0]][cell[1]] = list(domain)[0]

    def solve(self):
        """Solve the Sudoku puzzle."""
        if not self.apply_arc_consistency():
            return False
        self.assign_singletons() # comment this
        # result = self.backtrack()
        # if result:
        #    self.assign_singletons()
        #    return True
        # return False
        return self.backtrack()

    def backtrack(self):

        # solution found
        if all(len(self.domains[var]) == 1 for var in self.variables):
            return True

        if any(len(self.domains[var]) == 0 for var in self.variables):
            return False

        # Select unassigned variable with minimum remaining values
        var = min((v for v in self.variables if len(self.domains[v]) > 1), key=lambda v: len(self.domains[v]))

        to_be_shuffled_values = list(self.domains[var])
        random.shuffle(to_be_shuffled_values)

        # for value in self.domains[var]:
        for value in to_be_shuffled_values:
            snapshot = copy.deepcopy(self.domains)
            self.domains[var] = {value}
            if self.apply_arc_consistency():
                self.assign_singletons()  # comment this

                if self.backtrack():
                    return True
            self.domains = snapshot
        return False

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

puzzle2 = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0]
]


solver = SudokuSolverCSP(puzzle2)
if solver.solve():
    print("Sudoku solved:")
    for row in solver.puzzle:
        print(row)
else:
    print("No solution exists.")
