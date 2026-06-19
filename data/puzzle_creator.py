import json
import random as rd
from copy import deepcopy
from typing import List, Dict, Tuple, Optional
import os

from data.sudoku_generator import generate_filled_grid, init_used_arrays, find_best_empty_cell, place, remove

Grid = List[List[int]]

# These difficulty settings can be adjusted
DIFFICULTY_CONFIG = {
    "easy":   {"min_clues": 46, "max_clues": 51, "max_backtracks": 5},
    "medium": {"min_clues": 36, "max_clues": 45, "max_backtracks": 20},
    "hard":   {"min_clues": 28, "max_clues": 35, "max_backtracks": 50},
    "expert": {"min_clues": 22, "max_clues": 27, "max_backtracks": 100},
}

def count_solutions(grid: Grid, row_used, col_used, box_used, limit: int = 2) -> int:
    """
    Count the number of solutions for a given Sudoku grid, up to a specified limit.

    Parameters:
        grid (Grid): The Sudoku grid.
        row_used: Boolean array representing the values in each row.
        col_used: Boolean array representing the values in each col.
        box_used: Boolean array representing the values in each 3x3 box.
        limit (int): The maximum number of solutions to count before stopping early.

    Returns:
        int: The number of solutions found, up to the specified limit.
    """
    # Find the next best empty cell
    next = find_best_empty_cell(grid, row_used, col_used, box_used)

    # If there is none, then there's only one solution, return 1
    if next == None:
        return 1
    
    # Otherwise, store the tuple's data
    row, col, values = next

    # Count possible solutions through backtracking
    sol_count = 0
    for val in values:
        place(grid, row_used, col_used, box_used, row, col, val)
        sol_count += count_solutions(grid, row_used, col_used, box_used, limit)
        remove(grid, row_used, col_used, box_used, row, col, val)

        # If we find more than one solution, stop and return 2
        if sol_count >= 2:
            return 2
        
    return sol_count


def has_unique_solution(grid: Grid) -> bool:
    """
    Check whether a Sudoku grid has exactly one valid solution;
    wrapper function for count_solutions. 

    Parameters:
        grid (Grid): The Sudoku grid.

    Returns:
        bool: True if the grid has exactly one solution, False otherwise.
    """
    row_used, col_used, box_used = init_used_arrays(grid)

    return count_solutions(grid, row_used, col_used, box_used, 2) == 1


def remove_cells(filled_grid: Grid, difficulty: str) -> Tuple[Grid, Dict]:
    """
    Remove cells from a filled Sudoku grid to create a puzzle matching the
    requested difficulty level.

    Parameters:
        filled_grid (Grid): A completely filled valid Sudoku grid.
        difficulty (str): The target difficulty level. One of: easy, medium, hard, expert.

    Returns:
        Tuple[Grid, Dict]: The incomplete puzzle grid and a metadata dictionary
        containing the difficulty label, clue count, and backtrack count.
    """
    # Store settings for requested difficulty
    difficulty_config = DIFFICULTY_CONFIG[difficulty]
    min_clues = difficulty_config["min_clues"]
    max_clues = difficulty_config["max_clues"]
    max_backtracks = difficulty_config["max_backtracks"]

    grid_copy = deepcopy(filled_grid)
    row_used, col_used, box_used = init_used_arrays(grid_copy)
    
    # Make a shuffled list of all 81 cell positions
    shuffled_cell_pos = []
    for row in range(9):
        for col in range(9):
            shuffled_cell_pos.append((row, col))
    rd.shuffle(shuffled_cell_pos)
    
    backtracks = 0
    cells_removed = 0
    clues = 81

    for pos in shuffled_cell_pos:
        row, col = pos
        # Store the value and remove it from the cell
        curr_value = grid_copy[row][col]
        remove(grid_copy, row_used, col_used, box_used, row, col, curr_value)

        # If there's only one solution, increment cells_removed
        if has_unique_solution(grid_copy):
            cells_removed += 1
            clues -= 1

            # If no longer within difficulty parameters, undo removal 
            # and return grid and metadata
            if clues < min_clues or clues > max_clues or backtracks > max_backtracks:
                place(grid_copy, row_used, col_used, box_used, row, col, curr_value)
                clues += 1
                metadata = {"difficulty": difficulty, "clues": clues, "backtracks": backtracks}
                return grid_copy, metadata
        # If there is more than one solution, undo removal, increment backtracks,
        # and check if within difficulty parameters
        else: 
            place(grid_copy, row_used, col_used, box_used, row, col, curr_value)
            backtracks += 1

            # If no longer within difficulty parameters, return grid and metadata
            if backtracks > max_backtracks:
                backtracks -= 1
                metadata = {"difficulty": difficulty, "clues": clues, "backtracks": backtracks}
                return grid_copy, metadata

    # Done, return grid and metadata
    metadata = {"difficulty": difficulty, "clues": clues, "backtracks": backtracks}
    return grid_copy, metadata

def generate_puzzles(count: int, difficulty: str) -> List[Dict]:
    """
    Generate a specified number of Sudoku puzzles at the requested difficulty level.

    Parameters:
        count (int): The number of puzzles to generate.
        difficulty (str): The target difficulty level. One of: easy, medium, hard, expert.

    Returns:
        List[Dict]: A list of puzzle dictionaries, each containing the puzzle grid,
        solution grid, difficulty label, clue count, and backtrack count.
    """
    puzzles = []

    difficulty_config = DIFFICULTY_CONFIG[difficulty]
    min_clues = difficulty_config["min_clues"]
    max_clues = difficulty_config["max_clues"]
    max_backtracks = difficulty_config["max_backtracks"]

    while len(puzzles) < count:
        filled_grid = generate_filled_grid()
        puzzle, metadata = remove_cells(filled_grid, difficulty)

        # Check that the puzzle generated fits the diffiulty requirements
        # Store it if it does, otherwise, go to next loop
        if metadata["clues"] >= min_clues and metadata["clues"] <= max_clues and metadata["backtracks"] <= max_backtracks:
            puzzles.append({
                "puzzle": puzzle,
                "solution": filled_grid,
                "difficulty": difficulty,
                "clues": metadata["clues"],
                "backtracks": metadata["backtracks"]
            })

    return puzzles

def save_puzzles(puzzles: List[Dict], difficulty: str, chunk_size: int = 1000) -> None:
    """
    Save generated puzzles to JSON files in the data/metadata/ directory,
    split into chunks of a specified size. Files are named by difficulty and
    chunk number, e.g. easy_001.json.

    Parameters:
        puzzles (List[Dict]): The list of puzzle dictionaries to save.
        difficulty (str): The difficulty label used for naming the output files.
        chunk_size (int): The number of puzzles per file. Defaults to 1000.

    Returns:
        None
    """
    