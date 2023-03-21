import math
import numpy as np
import tkinter as tk
from tkinter import messagebox


class SudokuGUI(tk.Frame):
    def __init__(self, master: tk.Tk, title: str, size: int = 9) -> None:
        """
        Initializes the SudokuGUI object.

        Args:
            master (tk.Tk): The root window of the GUI.
            title (str): The title of the GUI.
            size (int): The size of the Sudoku puzzle. Default is 9.

        Attributes:
            master (tk.Tk): The root window of the GUI.
            size (int): The size of the Sudoku puzzle.
            box_size (int): The size of each sub-box in the puzzle.
            cells (list): A 2D list of Entry widgets representing the cells on the screen.
            board (list): A 2D list of integers representing the values on the screen at any time.
            solution (list): A 2D list of integers representing the solution to the puzzle on the screen.
            empty (list): A 2D list of integers representing the indices of the positions to be filled in the puzzle.

        Returns:
            None
        """
        tk.Frame.__init__(self, master)
        self.master = master
        self.master.title(title)
        self.grid()

        self.size = size
        self.box_size = int(math.sqrt(self.size))

        # Initialize self.cells
        self.create_cells()

        # Initialize self.board, self.solution, self.empty
        self.set()

        self.create_buttons()

    def check_row(self, row: int, num: int) -> bool:
        """
        Checks if a given number is valid in a given row of the Sudoku board.

        Args:
            row (int): The index of the row to check.
            num (int): The number to check.

        Returns:
            bool: True if the number is valid in the given row, False otherwise.
        """
        return num not in self.board[row]

    def check_col(self, col: int, num: int) -> bool:
        """
        Checks if a given number is valid in a given column of the Sudoku board.

        Args:
            col (int): The index of the column to check.
            num (int): The number to check.

        Returns:
            bool: True if the number is valid in the given column, False otherwise.
        """
        return num not in self.board[:, col]

    def check_box(self, row_start: int, col_start: int, num: int) -> bool:
        """
        Checks if a given number is valid in a given box of the Sudoku board.

        Args:
            row_start (int): The starting index of the row of the box to check.
            col_start (int): The starting index of the column of the box to check.
            num (int): The number to check.

        Returns:
            bool: True if the number is valid in the given box, False otherwise.
        """
        return num not in self.board[row_start : row_start + self.box_size, col_start : col_start + self.box_size]

    def is_valid(self, row: int, col: int, num: int) -> bool:
        """
        Checks if a given number is valid in a given position of the Sudoku board.

        Args:
            row (int): The index of the row to check.
            col (int): The index of the column to check.
            num (int): The number to check.

        Returns:
            bool: True if the number is valid in the given position, False otherwise.
        """
        return (
            self.check_row(row, num) and
            self.check_col(col, num) and
            self.check_box(row - row % self.box_size, col - col % self.box_size, num)
        )

    def set(self) -> None:
        """
        Sets the initial values of the board by generating a Sudoku puzzle and sets the cells on the GUI to match the generated board

        Returns:
            None
        """

        def fill_box(row_start: int, col_start: int) -> None:
            """
            Fill a 3x3 box with random numbers.

            Args:
                row_start (int): The starting row index of the box.
                col_start (int): The starting column index of the box.

            Returns:
                None
            """
            box = np.random.permutation(self.size) + 1
            self.board[row_start:row_start+self.box_size, col_start:col_start+self.box_size] = box.reshape((self.box_size, self.box_size))

        def fill_diagonal() -> None:
            """
            Fill the diagonal boxes of the Sudoku board with random numbers.

            The diagonal boxes are the 3x3 boxes that are located on the diagonal of the board.

            Returns:
                None
            """
            for i in range(0, self.size, self.box_size):
                fill_box(i, i)

        def fill_remaining(row: int, col: int) -> bool:
            """
            Recursively fill the remaining empty cells of the Sudoku board, skipping the cells that are already filled.

            Args:
                row (int): The row index of the cell to be filled.
                col (int): The column index of the cell to be filled.
            
            Returns:
                bool: True if all the empty cells have been filled with valid numbers, False otherwise.
            """
            
            # Move to the next row if we have reached the end of the current row
            if col == self.size:
                row += 1
                col = 0

            # Check if we have reached the end of the matrix
            if row == self.size:
                return True

            # Skip cells whose box is in the diagonal because they are already filled
            if self.board[row][col] != 0:
                return fill_remaining(row, col + 1)

            # Try filling the current cell with a valid value
            for num in range(1, self.size + 1):
                if self.is_valid(row, col, num):
                    self.board[row][col] = num
                    if fill_remaining(row, col + 1):
                        return True
                    self.board[row][col] = 0

            # No valid value was found, so backtrack
            return False

        def set_empty(leftover: int) -> None:
            """
            Initialize self.empty to a list of indices whose values have to be removed.

            Args:
                leftover (int): The number of cells in the board that should be left with values.

            Returns:
                None
            """
            
            # Total number of cells in the board
            total = self.size ** 2

            # Storing the (random) indices where digits are removed from the board as an attribute
            self.empty = np.random.choice(total, total - leftover, replace = False)

        def generate_board() -> None:
            """
            Generates a new Sudoku board.

            This function generates a Sudoku board using a recursive backtracking algorithm, starting by filling the diagonal 3x3 matrices with
            random numbers that pass the box check only since all 3x3 matrices in a diagonal are independent of other 3x3 adjacent matrices
            initially, as others are empty. Then, it recursively fills the remaining empty cells on the board by trying valid numbers for each cell,
            and backtracking if no valid number can be found.

            After generating the solved board, the function removes some of the digits from the board to create a puzzle. The number of digits
            removed is randomly chosen between 17 and 36, since a sudoku board needs a minimum of 17 clues for it to have a unique solution and
            most sudoku puzzles have 22-36 clues. self.empty is set a list of the locations of the digits that are removed.

            Returns:
                None
            """
            # Create an empty Sudoku board
            self.board = np.zeros((self.size, self.size), dtype = int)
            
            # Fill the diagonal 3x3 matrices
            fill_diagonal()
            
            # Fill the remaining cells on the board starting from position (0, 0)
            fill_remaining(0, 0)
            
            # Save the solution to the board
            self.solution = np.copy(self.board)

            # Set self.empty a list of 17-36 random indices
            set_empty(np.random.randint(17, 37))

            # Set the values at the calculated indicies to 0
            self.clear()

        # Generate a Sudoku board and set the cells on the GUI
        generate_board()
        self.set_cells()

    def set_cells(self, original_board: bool = True) -> None:
        """
        Sets the cells on the GUI based on the current state of the board.

        Args:
            original_board (bool): A flag that determines whether to use the original board or the solution board.
                Defaults to True, which means the original board will be used.

        Returns:
            None
        """
        
        # Determine which board (original or solution) to use
        board = self.board if original_board else self.solution
        
        # Determine foreground colors for each cell
        fg_colors = np.where(self.board == 0, "blue", "black")
        
        # Convert the board to a string array for inserting into the cells
        cell_values = np.where(board != 0, board.astype(str), "")

        # Loop through each cell in the GUI and update its properties
        for i in range(self.size):
            for j in range(self.size):
                
                # Clear the cell
                cell = self.cells[i][j]
                cell.config(state = "normal")
                cell.delete(0, tk.END)

                # Update the cell's foreground color and value
                cell.config(fg = fg_colors[i][j])
                cell.insert(0, cell_values[i][j])
                
                # Disable the cell if it already has a value
                if cell_values[i][j]:
                    cell.config(state = "disabled")

    def check_cell(self, event: tk.Event) -> None:
        """
        Change the attributes of the cell based on user input when a key is released.

        Args:
            event (tk.Event): The key event that triggered the function.

        Returns:
            None
        """
        
        # Get necessary values
        widget = event.widget
        num = widget.get()
        row = widget.grid_info()["row"]
        col = widget.grid_info()["column"]
        
        # Set the text color of the cell based on whether the current value is valid or not
        widget.config(fg = "green" if num.isdigit() and self.is_valid(row, col, int(num)) else "red")

        # Change value in self.board to reflect screen
        self.board[row][col] = 0 if not num else int(num)

        def board_match() -> bool:
            """
            Check if the current state of the board matches the solution.

            Returns:
                bool: True if the current state of the board matches the solution, False otherwise.
            """
            # Create a 2D numpy array of the current state of the board
            board_array = np.array([[int(widget.get()) if widget.get() else 0 for widget in row] for row in self.cells])
            
            # Check if the board array matches the solution array
            return np.array_equal(board_array, self.solution)
        
        # If the board matches the solution, ask the user if they want to play again and reset the board if they do
        if board_match() and messagebox.askyesno("Congratulations", "You have won! Do you want to play again?", icon = "question"):
            self.set()

    def create_cells(self) -> None:
        """
        Create and display the Entry widgets representing the cells of the sudoku board on the screen.

        Args:
            None

        Returns:
            None
        """
        
        self.cells = []
        for i in range(self.size):
            row = []
            for j in range(self.size):
                
                # Determine the background color for the cell based on the box it is in
                # White for an odd box, light gray for an even box 
                color = 'white' if (i // self.box_size + j // self.box_size) % 2 == 0 else 'light gray'
                
                # Create an Entry widget for the cell with the appropriate settings
                cell = tk.Entry(self,
                    width = 2,
                    font = ('Arial', 24, 'bold'),
                    justify = "center",
                    validate = "key",
                    validatecommand = (self.register(lambda n: n.isdigit() and int(n) >= 1 and int(n) <= self.size or n == ""), '%P'),
                    bg = color,
                    disabledbackground = '',
                    disabledforeground = '',
                    highlightthickness = 1,
                    highlightcolor = 'black'
                )
                
                # Add the widget to the grid and bind the check_cell method to the widget's KeyRelease event
                cell.grid(row = i, column = j)
                cell.bind("<KeyRelease>", self.check_cell)
                row.append(cell)
            self.cells.append(row)

    def clear(self) -> bool:
        """
        Clear the values at the chosen indices from the board.

        Returns:
            bool: True
        """
        self.board.flat[self.empty] = 0
        return True

    def create_buttons(self) -> None:
        """
        Creates and displays the buttons for the Sudoku board.

        Returns:
            None
        """

        # Create a "Clear" button and add it to the screen
        self.clear_button = tk.Button(self, text = "Clear", command = lambda: self.clear() and self.set_cells())
        self.clear_button.grid(row = self.size, column = 0 * self.box_size, columnspan = self.box_size)

        # Create a "Reset" button and add it to the screen
        self.reset_button = tk.Button(self, text = "Reset", command = self.set)
        self.reset_button.grid(row = self.size, column = 1 * self.box_size, columnspan = self.box_size)

        # Create a "Solve" button and add it to the screen
        self.solve_button = tk.Button(self, text = "Solve", command = lambda: self.set_cells(False))
        self.solve_button.grid(row = self.size, column = 2 * self.box_size, columnspan = self.box_size)


# Driver code
if __name__ == "__main__":
    root = tk.Tk()
    app = SudokuGUI(root, "Sudoku Solver")
    app.mainloop()
