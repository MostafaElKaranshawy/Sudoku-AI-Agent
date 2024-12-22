import customtkinter as ctk
from tkinter import messagebox
import numpy as np
from functools import partial

# Sudoku Solver using Backtracking Algorithm
def solve_sudoku(board):
    empty = find_empty(board)
    if not empty:
        return True
    row, col = empty

    for num in range(1, 10):
        if is_valid(board, num, row, col):
            board[row][col] = num
            if solve_sudoku(board):
                return True
            board[row][col] = 0

    return False

def find_empty(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return i, j
    return None

def is_valid(board, num, row, col):
    for i in range(9):
        if board[row][i] == num or board[i][col] == num:
            return False

    box_row = row // 3 * 3
    box_col = col // 3 * 3
    for i in range(box_row, box_row + 3):
        for j in range(box_col, box_col + 3):
            if board[i][j] == num:
                return False

    return True

def is_valid_board(board):
    def is_valid_placement(board, num, row, col):
        # Check row
        if num in board[row]:
            return False

        # Check column
        if num in [board[r][col] for r in range(9)]:
            return False

        # Check 3x3 grid
        box_row = (row // 3) * 3
        box_col = (col // 3) * 3
        for r in range(box_row, box_row + 3):
            for c in range(box_col, box_col + 3):
                if board[r][c] == num:
                    return False

        return True

    # Iterate through each cell in the board
    for row in range(9):
        for col in range(9):
            num = board[row][col]
            if num != 0:  # Skip empty cells
                # Temporarily set the cell to 0 to avoid false positives
                board[row][col] = 0
                if not is_valid_placement(board, num, row, col):
                    return False
                # Restore the number
                board[row][col] = num
    print(board)
    print("valid")
    return True


def is_board_complete_and_valid(board):
    """
    Check if the board is complete and valid.
    """
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:  # If there's any empty cell, the board is not complete
                return False
            if not is_valid(board, board[i][j], i, j):  # Validate the current value
                return False
    return True


class SudokuApp:
    def __init__(self):
        self.main_menu_button = None
        self.solve_button = None
        self.difficulty = None
        self.game_mode = None
        self.app = ctk.CTk()
        self.app.title("Sudoku")
        self.app.geometry("1000x1000")
        self.board = np.zeros((9, 9), dtype=int)

        self.main_menu()

    def main_menu(self):
        for widget in self.app.winfo_children():
            widget.destroy()

        self.app.grid_rowconfigure(0, weight=1)
        self.app.grid_rowconfigure(1, weight=1)
        self.app.grid_rowconfigure(2, weight=1)
        self.app.grid_columnconfigure(0, weight=1)

        frame = ctk.CTkFrame(self.app)
        frame.grid(row=1, column=0, padx=20, pady=20)

        ctk.CTkLabel(frame, text="Sudoku", font=("Arial", 40)).pack(pady=20)

        mode_frame = ctk.CTkFrame(frame, width=500)
        mode_label = ctk.CTkLabel(mode_frame, text="Mode", font=("Arial", 24))
        mode_label.pack(pady=20, side="left", padx=10)

        self.game_mode = ctk.StringVar(value="Random Board")
        options_menu = ctk.CTkOptionMenu(mode_frame, values=["Random Board", "Custom Board", "User Mode"],
                                         variable=self.game_mode, font=("Arial", 20))
        options_menu.pack(pady=20, side="right", padx=10)
        mode_frame.pack(pady=10)

        difficulty_frame = ctk.CTkFrame(frame, width=400)
        self.difficulty = ctk.StringVar(value="Easy")

        difficulty_label = ctk.CTkLabel(difficulty_frame, text="Select Difficulty", font=("Arial", 24))
        difficulty_label.pack(pady=10, side="left", padx=10)
        difficulty_menu = ctk.CTkOptionMenu(difficulty_frame, values=["Easy", "Medium", "Hard"],
                                            variable=self.difficulty, font=("Arial", 20))
        difficulty_menu.pack(pady=20, side="right", padx=10)
        difficulty_frame.pack(pady=10)

        start_button = ctk.CTkButton(frame, text="Start Game", command=self.start_game,
                                     font=("Arial", 24), fg_color="green")
        start_button.pack(pady=10)

        exit_button = ctk.CTkButton(frame, text="Exit Game", command=self.exit,
                                    font=("Arial", 24), fg_color="red")
        exit_button.pack(pady=10)


    def start_game(self):

        if self.game_mode.get() == "Random Board":
            self.generate_board()
            self.show_board(mode=1)
        elif self.game_mode.get() == "Custom Board":
            self.clear_board()
            self.show_board(mode=2)
        elif self.game_mode.get() == "User Mode":
            self.generate_board()
            self.show_board(mode=3)
            self.handle_user_mode()

    def generate_board(self):
        # self.update_idletasks()
        self.clear_board()
        # self.update_idletasks()
        # Generate a full valid board
        self.generate_full_board()

        # Remove numbers based on difficulty while ensuring a unique solution
        difficulty_map = {"Easy": 30, "Medium": 40, "Hard": 50}
        cells_to_remove = 81 - difficulty_map[self.difficulty.get()]
        removed_cells = []

        while len(removed_cells) < cells_to_remove:
            row, col = np.random.randint(0, 9, size=2)
            if (row, col) not in removed_cells:
                temp = self.board[row][col]
                self.board[row][col] = 0
                temp_board = np.copy(self.board)
                solution_count = self.count_solutions(temp_board)
                if solution_count == 1:
                    removed_cells.append((row, col))
                else:
                    self.board[row][col] = temp

    def generate_full_board(self):
        def fill_board(board):
            empty = find_empty(board)
            if not empty:
                return True
            row, col = empty

            numbers = list(range(1, 10))
            np.random.shuffle(numbers)
            for num in numbers:
                if is_valid(board, num, row, col):
                    board[row][col] = num
                    if fill_board(board):
                        return True
                    board[row][col] = 0

            return False

        fill_board(self.board)

    def count_solutions(self, board):
        # Helper function to count the number of solutions
        def backtrack(board):
            empty = find_empty(board)
            if not empty:
                return 1
            row, col = empty

            count = 0
            for num in range(1, 10):
                if is_valid(board, num, row, col):
                    board[row][col] = num
                    count += backtrack(board)
                    board[row][col] = 0
                    if count > 1:  # Stop early if more than one solution is found
                        break
            return count

        return backtrack(board)

    def clear_board(self):
        self.board = np.zeros((9, 9), dtype=int)

    def show_board(self, mode):
        for widget in self.app.winfo_children():
            widget.destroy()

        self.app.grid_rowconfigure(0, weight=1)
        self.app.grid_rowconfigure(1, weight=1)
        self.app.grid_rowconfigure(2, weight=1)
        self.app.grid_columnconfigure(0, weight=1)

        frame = ctk.CTkFrame(self.app)
        frame.grid(row=1, column=0, padx=20, pady=20)

        self.cells = []
        for i in range(9):
            row = []
            for j in range(9):
                value = self.board[i][j]
                color = "black" if value != 0 else "gray"
                entry = ctk.CTkEntry(frame, width=80, height=80, justify="center", fg_color=color, font=("Arial", 20))
                entry.insert(0, value if value != 0 else "")
                entry.configure(state="disabled" if value != 0 or mode == 1 else "normal")
                padx = 12 if j % 3 == 0 else 3
                pady = 12 if i % 3 == 0 else 3

                entry.grid(row=i, column=j, padx=(padx, 3), pady=(pady, 3))
                row.append(entry)
            self.cells.append(row)

        button_frame = ctk.CTkFrame(frame)
        button_frame.grid(row=10, column=0, columnspan=9, pady=10)

        self.solve_button = ctk.CTkButton(button_frame, text="Solve", command=self.solve_gui, font=("Arial", 24))
        self.solve_button.grid(row=0, column=0, padx=10)
        self.main_menu_button = ctk.CTkButton(button_frame, text="Main Menu", command=self.back_to_main_menu,
                                              font=("Arial", 24), fg_color="red")
        self.main_menu_button.grid(row=0, column=1, padx=10)

        if mode == 2:
            ctk.CTkLabel(frame, text="Input your board representation, then click Solve").grid(row=11, column=0,
                                                                                               columnspan=9, pady=10)
    def back_to_main_menu(self):
        if messagebox.askyesno(title="Main Menu", message= "Back to Main Menu?"):
            self.main_menu()
        else:
            return
    def solve_gui(self):
        solved_board = np.copy(self.board)
        for i in range(9):
            for j in range(9):
                if self.cells[i][j].get().isdigit():
                    self.board[i][j] = int(self.cells[i][j].get())

        if not is_valid_board(self.board):
            messagebox.showerror(title="Invalid Board", message="Each number in the board cannot be repeated in a row, "
                                                               "a column or in a 3x3 grid")
            return

        if solve_sudoku(self.board):
            for i in range(9):
                for j in range(9):
                    if solved_board[i][j] == 0:  # Only highlight solved cells
                        self.cells[i][j].delete(0, "end")
                        self.cells[i][j].configure(state="normal")

                        self.cells[i][j].insert(0, self.board[i][j])
                        self.cells[i][j].configure(fg_color="green")
                        self.cells[i][j].configure(state="disabled")

                    else:
                        self.cells[i][j].configure(fg_color="black")

            self.solve_button.configure(text="New Game", command=self.start_game)
        else:
            messagebox.showerror("Error", "No solution exists for the provided board.")

    def handle_user_mode(self):
        self.solve_button.configure(state="disabled")
        solved_board = np.copy(self.board)
        solve_sudoku(solved_board)
        def validate_input(event, row, col):
            print(solved_board)

            cell = event.widget

            value = cell.get()
            print(value)
            # Reset board cell if input is invalid
            if value == '':
                self.cells[row][col].configure(fg_color="gray")
                self.board[row][col] = 0
                return

            if not 1 <= int(value) <= 9:
                self.cells[row][col].configure(fg_color="red")
                self.board[row][col] = 0
                print("error")
                return

            num = int(value)
            self.board[row][col] = num  # Temporarily update the board for validation

            # Validate current move
            if num != solved_board[row][col]:
                self.cells[row][col].configure(fg_color="red")
                self.board[row][col] = 0  # Reset the cell in the board
                print("wrong")
            else:
                self.cells[row][col].configure(fg_color="green")
                self.cells[row][col].configure(state="disabled")

                print("true")
                # Check if the board is complete and valid
                if is_board_complete_and_valid(self.board):
                    messagebox.showinfo("Congratulations!", "You successfully completed the Sudoku!")
        is_board_complete_and_valid(self.board)
        for i in range(9):
            for j in range(9):
                    self.cells[i][j].bind("<KeyRelease>", partial(validate_input,row=i, col=j))

    def run(self):
        self.app.mainloop()
    def exit(self):
        if messagebox.askyesno(title="Exit Game", message="Are you sure you want to exit?"):
            exit()
        else:
            return
if __name__ == "__main__":
    app = SudokuApp()
    app.run()
