"""
It is convenient to have a procedure that accepts both a search algorithm and a heuristic function 
(e.g., `IDA*` + Manhattan distance) as parameters, runs tests, and saves the results for subsequent analysis.

The `massive_test` function presumes that the search function adheres to the following template:

```
search(start_state, goal_state, *optional arguments*) -> (path_found, last_state, steps, search_tree_size)
```
where
- `start_state/goal_state` — start and goal states, in the form of `GemPuzzleState`
- `*optional arguments*` — additional parameters of the search function, passed usin `*args`. 
    For instance, the heuristic function.
- `path_found` — `True` if path was found, `False` otherwise
- `last_state` — last state of the path. `None` if path was not found
- `steps` —  the number of search steps
- `search_tree_size` — the number of nodes that compose the search tree at the final iteration of the algorithm 
    (=the size of the resultant search tree)
"""

from typing import Callable, Dict
import traceback
import numpy as np
from utils.gem_puzzle import GemPuzzleState


def massive_test(search_function: Callable, data_path: str, *args) -> Dict:
    """
    The `massive_test` function runs the `search_function` on a set of different tasks
    (for example, from the directory `data/`) using *args as optional arguments.

    The function returns a dictionary containing statistics with the following keys:
     - "len" — the length of each path (0.0 if a path wasn't found).
     - "st_size" — the size of the resultant search tree for each task.
     - "steps" — the number of algorithm steps for each task.

    Parameters
    ----------
    search_function : Callable
        The implemented search method.
    data_path : str
        Path to the directory containing tasks.

    Returns
    -------
    stat : Dict
        A dictionary containing statistics.
    """

    stat = {
        "len": [],
        "st_size": [],
        "steps": [],
    }

    with open(data_path) as tasks_file:
        for task_num, line in enumerate(tasks_file):
            if not line.strip():
                continue

            start_tile_list = list(map(int, line.split()))
            goal_tile_list = list(range(1, len(start_tile_list) + 1))
            start_state = GemPuzzleState(start_tile_list)
            goal_state = GemPuzzleState(goal_tile_list)

            try:
                found, last_state, number_of_steps, search_tree_size = search_function(
                    start_state, goal_state, *args
                )

                if found:
                    stat["len"].append(last_state.g)
                else:
                    stat["len"].append(0.0)

                stat["st_size"].append(search_tree_size)
                stat["steps"].append(number_of_steps)

            except Exception as e:
                print(f"Task: #{task_num}. Execution error: {e}")
                traceback.print_exc()

    return {k: np.array(v) for k, v in stat.items()}
