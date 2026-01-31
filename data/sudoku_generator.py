import random as rd
from typing import List, Optional, Tuple

Grid = List[List[int]]

def create_empty_grid() -> Grid:
    """
    Create a 9x9 Sudoku grid filled with zeroes.

    Returns:
        Grid: An empty 9x9 grid.
    """
    grid: Grid = []

    for _ in range(9):
        row: List[int] = [0] * 9
        grid.append(row)

    return grid

def find_empty_cell(grid: Grid) -> Optional[Tuple[int, int]]:
    """
    Find the next empty cell in the grid.

    Parameters:
        grid (Grid): The Sudoku grid.

    Returns:
        Optional[Tuple[int, int]]: A tuple (row, col) of the next empty cell,
        or None if the grid is full.
    """
    for row in range(9):
        for col in range(9):
            if grid[row][col] == 0:
                return row, col
            
    return None

def is_valid_move(grid: Grid, row: int, col: int, value: int) -> bool:
    """
    Check whether placing a value at (row, col) follows Sudoku rules.

    Parameters:
        grid (Grid): The Sudoku grid.
        row (int): Row index of the cell.
        col (int): Column index of the cell.
        value (int): Value to validate (1–9).

    Returns:
        bool: True if the move is valid, False otherwise.
    """
    # If the cell is currently empty
    if grid[row][col] == 0:
        # Check if the value is already in the row
        for c in range(9):
            if (grid[row][c] == value):
                return False

        # Check if the value is already in the col
        for r in range(9):
            if (grid[r][col] == value):
                return False

        # Now check the 3x3 box
        box_corner_row = (row // 3) * 3
        box_corner_col = (col // 3) * 3

        for r in range(box_corner_row, box_corner_row + 3):
            for c in range(box_corner_col, box_corner_col + 3):
                if (grid[r][c] == value):
                    return False

        # If the value is currently not in row, col, or 3x3 box, valid move
        return True
    
    # Otherwise, invalid move
    return False

def fill_grid(grid: Grid) -> bool:
    """
    Fill up the grid as per Sudoku rules.

    Parameters:
        grid (Grid): The Sudoku grid.

    Returns:
        bool: True if the grid is successfully filled.
    """
    # Variable declaration/initialization
    next_cell =  find_empty_cell(grid)
    values = list(range(1, 10))
    rd.shuffle(values)
    
    # Base case
    if next_cell is None:
        return True
    
    # Otherwise, fill up the cell
    row, col = next_cell

    for val in values:
        if is_valid_move(grid, row, col, val):
            grid[row][col] = val

            if fill_grid(grid):
                return True
            grid[row][col] = 0
    
    return False

def is_valid_group(values: List[int]) -> bool:
    """
    Validates that a given group of 9 digits has no zeroes and no repeat numbers.

    Parameters:
        values (List): 9 digits taken from the Sudoku grid.

    Returns:
        bool: True if there are no repeat digits, False otherwise.
    """
    # Remove the zeroes 
    numbers = [n for n in values if n != 0]

    # Check for duplicates
    no_duplicates = len(numbers) == len(set(numbers))

    return no_duplicates

def is_valid_grid(grid: Grid) -> bool:
    """
    Validates that a given 9x9 Sudoku board has no zeroes and no illegal moves.

    Parameters:
        grid (Grid): The Sudoku grid.

    Returns:
        bool: True if the board is valid, False otherwise.
    """
    # Validate rows
    for row in grid:
        if not is_valid_group(row):
            return False

    # Validate columns
    for col in range(9):
        values = [grid[row][col] for row in range(9)]
        if not is_valid_group(values):
            return False
        
    # Validate 3x3 boxes
    for row in range(0, 9, 3):
        for col in range(0, 9, 3):
            values = [grid[r][c]
                      for r in range(row, row + 3)
                      for c in range(col, col + 3)]
            if not is_valid_group(values):
                return False
            
    # If everything is valid
    return True

def generate_filled_grid() -> Grid:
    """
    Generate a completely filled Sudoku grid.

    Returns:
        grid (Grid): The Sudoku grid.
    """
    while True:
        grid: Grid = create_empty_grid()
        fill_grid(grid)

        if is_valid_grid(grid):
            return grid
    
def main():
    grid: Grid = generate_filled_grid()
    for row in grid:
        print(row)

if __name__ == "__main__":
    main()