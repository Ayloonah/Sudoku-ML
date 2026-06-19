import random as rd
from typing import List, Optional, Tuple

Grid = List[List[int]]

def box_index(row: int, col: int) -> int:
    """
    Calculate the index of the 3x3 box the row & col index is in.

    Parameters:
        row (int): Row index of the cell.
        col (int): Column index of the cell.

    Returns:
        int: The index of the box we are looking at.
    """
    return (row // 3) * 3 + (col // 3)

def init_used_arrays(grid: Grid) -> Tuple[List[List[bool]], List[List[bool]], List[List[bool]]]:
    """
    From our grid, generate three used arrays that keep track of where
    the values currently are in the Sudoku grid.

    Parameters:
        grid (Grid): The Sudoku grid.

    Returns:
        Tuple[List[List[bool]], List[List[bool]], List[List[bool]]]:
        A tuple containing the three used arrays tracking the grid's values.
    """
    row_used = [[False] * 10 for _ in range(9)]
    col_used = [[False] * 10 for _ in range(9)]
    box_used = [[False] * 10 for _ in range(9)]

    # Store the grid's values within the used arrays
    for row in range(9):
        for col in range(9):
            value = grid[row][col]
            if value == 0:
                continue
            box = box_index(row, col)
            row_used[row][value] = True
            col_used[col][value] = True
            box_used[box][value] = True

    return row_used, col_used, box_used

def create_empty_grid() -> Grid:
    """
    Create a 9x9 Sudoku grid filled with zeroes.

    Returns:
        Grid: An empty 9x9 grid.
    """
    return [[0] * 9 for _ in range(9)]

def find_best_empty_cell(grid: Grid, row_used, col_used, 
                         box_used) -> Optional[Tuple[int, int, List[int]]]:
    """
    Find the empty cell in the grid with the fewest possible values, if any.

    Parameters:
        grid (Grid): The Sudoku grid.
        row_used: Boolean array representing the values in each row.
        col_used: Boolean array representing the values in each col.
        box_used: Boolean array representing the values in each 3x3 box.

    Returns:
        Optional[Tuple[int, int, List[int]]]: A tuple (row, col, int list) of the
        next best empty cell and its potential values, or None if the grid is full.
    """
    best_empty_cell = None
    best_empty_cell_values: List[int] = []
    
    # Find the cell with the least amount of possible valid moves
    for row in range(9):
        for col in range(9):
            # Skip the cell if it is not empty
            if grid[row][col] != 0:
                continue

            # Find the current cell's possible valid moves
            values = [val for val in range(1, 10) if 
                      is_valid_move(row_used, col_used, box_used, 
                                    row, col, val)]
            
            # If there are no possible values in this cell, return None
            if len(values) == 0:
                return None

            # Otherwise, recurse to find the empty cell with the least amount of values
            if best_empty_cell is None or len(values) < len(best_empty_cell_values):
                best_empty_cell = (row, col)
                best_empty_cell_values = values

                # If the cell can only hold one value, then return it right away
                if len(best_empty_cell_values) <= 1:
                    return row, col, best_empty_cell_values
    
    # If grid is full
    if best_empty_cell is None:
        return None
    
    # Once we've found the best empty cell, return it
    return best_empty_cell[0], best_empty_cell[1], best_empty_cell_values

def is_valid_move(row_used, col_used, box_used, row: int, col: int,
                   value: int) -> bool:
    """
    Check whether placing a value at (row, col) follows Sudoku rules.

    Parameters:
        row_used: Boolean array representing the values in each row.
        col_used: Boolean array representing the values in each col.
        box_used: Boolean array representing the values in each 3x3 box.
        row (int): Row index of the cell.
        col (int): Column index of the cell.
        value (int): Value to validate (1–9).

    Returns:
        bool: True if the move is valid, False otherwise.
    """
    # Find the box index
    box = box_index(row, col)

    # Return False if the value is in any of the three arrays, True otherwise
    return (not row_used[row][value]
            and not col_used[col][value]
            and not box_used[box][value])

def place(grid: Grid, row_used, col_used, box_used, row: int, col: int,
          value: int):
    """
    Place a value at the designated row, col index and updates the used arrays.

    Parameters:
        grid (Grid): The Sudoku grid.
        row_used: Boolean array representing the values in each row.
        col_used: Boolean array representing the values in each col.
        box_used: Boolean array representing the values in each 3x3 box.
        row (int): Row index of the cell.
        col (int): Column index of the cell.
        value (int): Value to validate (1–9).
    """
    grid[row][col] = value
    box = box_index(row, col)
    row_used[row][value] = True
    col_used[col][value] = True
    box_used[box][value] = True

def remove(grid: Grid, row_used, col_used, box_used, row: int, col: int,
          value: int):
    """
    Remove a value from the designated row, col index and updates the used arrays.

    Parameters:
        grid (Grid): The Sudoku grid.
        row_used: Boolean array representing the values in each row.
        col_used: Boolean array representing the values in each col.
        box_used: Boolean array representing the values in each 3x3 box.
        row (int): Row index of the cell.
        col (int): Column index of the cell.
        value (int): Value to validate (1–9).
    """
    grid[row][col] = 0
    box = box_index(row, col)
    row_used[row][value] = False
    col_used[col][value] = False
    box_used[box][value] = False

def fill_grid(grid: Grid, row_used, col_used, box_used) -> bool:
    """
    Fill up the grid.

    Parameters:
        grid (Grid): The Sudoku grid.
        row_used: Boolean array representing the values in each row.
        col_used: Boolean array representing the values in each col.
        box_used: Boolean array representing the values in each 3x3 box.

    Returns:
        bool: True if the grid is successfully filled.
    """
    # Check if there is an empty cell left
    next_cell = find_best_empty_cell(grid, row_used, col_used, box_used)
        
    # If none, return
    if next_cell is None:
        return True
    
    # If there is one, fill up the cell
    row, col, values = next_cell
    rd.shuffle(values)

    for val in values:
        place(grid, row_used, col_used, box_used, row, col, val)

        if fill_grid(grid, row_used, col_used, box_used):
            return True
        
        remove(grid, row_used, col_used, box_used, row, col, val)
    
    return False

def generate_filled_grid() -> Grid:
    """
    Generate a completely filled Sudoku grid.

    Returns:
        grid (Grid): The Sudoku grid.
    """
    grid: Grid = create_empty_grid()
    row_used, col_used, box_used = init_used_arrays(grid)
    fill_grid(grid, row_used, col_used, box_used)
    
    return grid
    
def main():
    grid: Grid = generate_filled_grid()
    for row in grid:
        print(row)

if __name__ == "__main__":
    main()