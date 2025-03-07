import random
from typing import Any
from unittest.mock import patch

import pytest

# pathfinding has no rigorous type checking
# so errors need to be supressed
from pathfinding.core.graph import Graph  # type: ignore
from pathfinding.finder.dijkstra import DijkstraFinder  # type: ignore

from generator.generators import generator_Adam
from generator.grid import Grid
from generator.maze import Maze


# checks if all area is filled
# and solution is found
def test_generator_Adam(capfd: pytest.CaptureFixture[str]) -> None:
    maze = Maze()
    start = (2, 3)
    end = (5, 7)
    # test if it catches an improperly set start/end
    with pytest.raises(ValueError):
        maze = generator_Adam(10, 10, (-2, 3), end, stop_coeff=100)
    assert maze.get_connections((0, 0)) == set()
    with pytest.raises(ValueError):
        maze = generator_Adam(10, 10, start, (5, 11), stop_coeff=100)
    assert maze.get_connections((0, 0)) == set()
    with pytest.raises(ValueError):
        maze = generator_Adam(10, 10, start, start, stop_coeff=100)
    assert maze.get_connections((0, 0)) == set()
    # test if properly started maze is fully filled
    maze = generator_Adam(10, 10, start, end, stop_coeff=100)
    grid = Grid(maze)
    grid.__debug_print__()
    out, err = capfd.readouterr()
    assert out.find("█") == -1
    # test if solution exists
    # two internal fors loop over all tiles and get
    # [tile_number, neighbour_number, 1 (weight of connection)]
    # the outer two flatten the list because tiles have different numbers of neighbours
    # node number for Dijkstra is made in a way of x+width*y everywhere below
    edges = [
        x
        for xs in [
            [
                [
                    node[0] + node[1] * maze.size()[0],
                    nghbr[0] + nghbr[1] * maze.size()[0],
                    1,
                ]
                for nghbr in nghbrs
            ]
            for node, nghbrs in maze.graph.items()
        ]
        for x in xs
    ]
    graph = Graph(edges=edges)
    finder = DijkstraFinder()
    path, runs = finder.find_path(
        graph.node(start[0] + start[1] * maze.size()[0]),
        graph.node(end[0] + end[1] * maze.size()[0]),
        graph,
    )
    assert path != []


def test_random_mocking_basic() -> None:
    with patch("random.choices", side_effect=lambda x: [x[1]]):
        assert random.choices([1, 2, 3])[0] == 2


# neede for the next test
# to avoid recursion, i preserve the original function under a different name
values_trial = 0
temp_random_choices = random.choices


def mock_random_choices_trial(*args: Any) -> list[int]:
    global values_trial
    if values_trial < 10:
        values_trial += 1
        return [0]
    return temp_random_choices(*args)


def function_containing_random_choice() -> int:
    return random.choices([1, 2, 3])[0]


# test if i can fake first 10 values
@patch("random.choices", new=mock_random_choices_trial)  # type: ignore
def test_random_mocking_advanced() -> None:
    for i in range(10):
        assert function_containing_random_choice() == 0
    temp_value = function_containing_random_choice()
    assert temp_value == 1 or temp_value == 2 or temp_value == 3


# reset of the value
values = 0


# local function for choosing random variable
def mock_random_choices(*args: Any) -> list[tuple[int, int]]:
    global values
    direction_list = [(0, 1), (1, 1), (2, 1), (2, 0), (1, 0)]
    if values < len(direction_list):
        temp_list = [direction_list[values]]
        values += 1
        return temp_list
    return temp_random_choices(*args)


# checks if upon dead end a new solution can be found
@patch("random.choices", new=mock_random_choices)  # type: ignore
def test_generator_Adam_dead_end_solution(capfd: pytest.CaptureFixture[str]) -> None:
    maze = generator_Adam(5, 2, (0, 0), (4, 1), towards_coeff=100)
    grid = Grid(maze)
    grid.__debug_print__()
    out, err = capfd.readouterr()
    assert out.find("█") == -1
