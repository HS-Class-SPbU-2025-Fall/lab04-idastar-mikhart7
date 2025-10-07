from typing import List, Optional
import copy
import numpy as np

class GemPuzzleState:
    """
    Implementing a search state (or simply, a state) in code is a crucial first step
    necessary for tackling any search problem. The `GemPuzzleState` class is structured
    with the following fields:

    Attributes
    ----------
    size : int
        Width of the game field.

    tile_list : Optional[List[int]]
        Tile positions represented as a list of integers from 1 to (size x size).
        Each integer corresponds to a tile's value, and its index represents its position
        on the game field. The tile with the maximum value is considered the blank.

    parent : GemPuzzleState
        A pointer to the parent state. The parent is a predecessor of the state in
        the search tree. It is used to reconstruct a path to that state from the start
        state (the root of the search tree).

    blank_pos : int
        The position of the empty tile in tile_list. Explicitly
        storing the position of a blank helps to generate successors faster.
    """

    def __init__(self, tile_list: Optional[List[int]] = None):
        """
        Constructor. Sets tile positions and performs some basic checks.

        Parameters
        ----------
        tile_list : List[int]
            Tile positions as a list of integers from 1 to `size * size`.
            The tile with value `size * size` represents the blank position.
        """
        if tile_list is None:
            self.size: int = None
            self.blank_pos: int = None
            return

        self.tile_list = tile_list
        self.size = int(len(tile_list) ** 0.5)

        if len(tile_list) != self.size**2:
            raise ValueError("Tile list size should be a perfect square.")

        # Finding the position of the blank tile
        blank_value = self.size**2
        self.blank_pos = self.tile_list.index(blank_value) if blank_value in self.tile_list else -1

        if self.blank_pos == -1:
            raise ValueError("State should contain max value indicating the blank tile's position.")

    def __eq__(self, other) -> bool:
        """
        Compares one state with another based on their tile lists.
        """
        return hash(self) == hash(other) and self.tile_list == other.tile_list

    def __str__(self) -> str:
        """
        Return a string representation of the game field for printing.
        """
        blank_value = self.size**2
        tile_matrix = np.array(self.tile_list).reshape(self.size, self.size)
        result = (
            str(tile_matrix).replace(" [", "").replace("[", "").replace("]", "").replace(str(blank_value), "_") + "\n"
        )
        return result

    def __hash__(self):
        return hash(str(self.tile_list))


def get_successors(state: GemPuzzleState) -> List[GemPuzzleState]:
    """
    Implementing the `get_successors` function is another crucial step in tackling any search problem.
    This function is designed to take a specific search state as input and return all possible successor states,
    which result from applying all applicable actions to the input state. In the case of GemPuzzle, the successors
    correspond to the board states resulting from moving the blank tile up, down, left, or right. If the blank tile
    goes out of the field after a move, such a successor should be discarded.

    Parameters
    ----------
    state : GemPuzzleState
        The input search state.

    Returns
    -------
    List[GemPuzzleState]
        A list containing all possible successor states for the input state.
    """
    successors = []
    delta = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    for dx, dy in delta:
        row = state.blank_pos // state.size
        col = state.blank_pos % state.size
        row += dx
        col += dy

        if 0 <= row < state.size and 0 <= col < state.size:
            new_state = GemPuzzleState()
            new_state.size = state.size
            new_state.tile_list = copy.copy(state.tile_list)
            new_state.blank_pos = row * state.size + col
            new_state.tile_list[state.blank_pos] = new_state.tile_list[new_state.blank_pos]
            new_state.tile_list[new_state.blank_pos] = state.size**2
            successors.append(new_state)

    return successors
