# Sudoku Solver

This code implements a Sudoku game with a graphical user interface. Each sudoku is generated automatically with a unique solution using the "backtracking" algorithm.

## Getting Started

### Prerequisites

This code requires Python 3 and the following packages:
1. numpy
2. tkinter

### Installation

1. Clone the repository: `git clone https://github.com/Suhana66/Sudoku-Solver.git`
2. Install the dependencies: `pip install -r requirements.txt`
3. Run the program: `python3 sudoku.py`

## How to play the game

The objective of the game is to fill a 9x9 grid with digits so that each column, each row, and each of the nine 3x3 subgrids contains all of the digits from 1 to 9. Each sudoku board has a unique solution

Once the game is running, a new sudoku puzzle is shown where users can enter a number between 1 and 9 in the cells of the board that have no values using the keyboard. The number entered turns green if the number is a valid entry in that cell and red if it is invalid. A valid entry can be defined that the number is not already present in the row, column or 3x3 box that the number is inputed.

The game includes 3 buttons- Clear, Reset and Solve. The 'Clear' button deletes all user input from the board and reverts the board to its initial state. The 'Reset' button generates a new board and displays it on the screen. The 'Solve' button displays the solution of the sudoku board on the screen

Once all the cells have been filled with valid numbers, the game is won and prompts the user if they want to play again

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
