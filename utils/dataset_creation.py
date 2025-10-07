from random import shuffle
from typing import List
import math

from utils.gem_puzzle import GemPuzzleState

def is_solvable(tile_list: List[int]) -> bool:
    """
    Checks that task is solvable.

    Parameters
    ----------
    tile_list : List[int]
        Tile positions represented as a list of integers. This list is expected to contain
        values from 1 to (size x size). Each integer value corresponds to a tile and
        the position in the list (index) corresponds to the position of the tile on the game field.
        Tile with the value (size x size) is assumed to represent blank position.

    Returns
    ----------
    bool
        Task is solvable.
    """
    inversions = 0
    puzzle_except_empty = [(i, v) for i, v in enumerate(tile_list) if v != len(tile_list)]

    for idx, (i, tile) in enumerate(puzzle_except_empty):
        for j, next_tile in puzzle_except_empty[idx + 1 :]:
            if next_tile < tile:
                inversions += 1

    size = int(math.sqrt(len(tile_list)))
    if size % 2 != 0 and inversions % 2 == 0:
        return True
    if size % 2 == 0:
        empty_row = size - tile_list.index(len(tile_list)) // size
        return (empty_row % 2 != 0) == (inversions % 2 == 0)
    return False


def generate_random_tile_list(size: int) -> List[int]:
    tile_list = [i + 1 for i in range(size**2)]
    shuffle(tile_list)
    return tile_list


def manhattan_distance(state1: GemPuzzleState, state2: GemPuzzleState) -> int:
    """
    Computes the Manhattan distance between two Gem Puzzle states. 
    The blank tile is not checked when calculating the Manhattan distance.

    Parameters
    ----------
    state1 : GemPuzzleState
        Representation of the first state.
    state2 : GemPuzzleState
        Representation of the second state.

    Returns
    ----------
    int
        Manhattan distance between two states.
    """
    size = state1.size
    blank_value = len(state1.tile_list)
    positions = {tile: pos2 for pos2, tile in enumerate(state2.tile_list) if tile != blank_value}
    dist_sum = 0

    for pos1, tile in enumerate(state1.tile_list):
        if tile != blank_value:
            pos2 = positions[tile]
            di = abs((pos1 // size) - (pos2 // size))
            dj = abs((pos1 % size) - (pos2 % size))
            dist_sum += di + dj
    return dist_sum


def get_manhattan_distance(tile_list: List[int]) -> int:
    goal_tile_list = list(range(1, len(tile_list) + 1))
    start_state = GemPuzzleState(tile_list)
    goal_state = GemPuzzleState(goal_tile_list)
    return manhattan_distance(start_state, goal_state)


def is_acceptable_task(tile_list: List[int], max_distance: int = 12) -> bool:
    if not is_solvable(tile_list):
        return False
    if get_manhattan_distance(tile_list) > max_distance:
        return False
    return True


def generate_tasks(task_file_path: str, number_of_tasks: int, size: int):
    """
    Generates number_of_tasks random tasks with specified size.

    Parameters
    ----------
    task_file_path : str
        Path to the file for writing tasks.
    number_of_tasks : int
        Required number of tasks to generate.
    size : int
        Required size of game fields in tasks.
    """
    with open(task_file_path, "a") as tasks_file:
        for _ in range(number_of_tasks):
            tile_list = generate_random_tile_list(size)

            while not is_acceptable_task(tile_list):
                tile_list = generate_random_tile_list(size)

            tasks_file.write(" ".join(map(str, tile_list)) + "\n")
            print(*tile_list, "Manhattan distance", get_manhattan_distance(tile_list))