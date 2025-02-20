import random
from unittest.mock import patch

import pytest

from generator.generators import generator_Adam
from generator.grid import Grid


# checks if all area is filled
# and solution is found (TODO: implement pathfinding, possibly from a package?)
def test_generator_Adam(capfd: pytest.CaptureFixture[str]) -> None:
    maze = generator_Adam(10, 10, (0, 0), (9, 9), stop_coeff=100)
    grid = Grid(maze)
    grid.__debug_print__()
    out, err = capfd.readouterr()
    assert out.find("█") == -1


# checks if upon dead end a new solution can be found
def test_generator_Adam_dead_end_solution(capfd: pytest.CaptureFixture[str]) -> None:
    maze = generator_Adam(2, 5, (0, 0), (4, 1), elsewhere_coeff=20, turn_coeff=20)
    grid = Grid(maze)
    grid.__debug_print__()
    out, err = capfd.readouterr()
    assert out.find("█") == -1


def test_random_mocking() -> None:
    with patch("random.choice", side_effect=lambda x: x[0]):
        assert random.choice([1, 2, 3]) == 1
