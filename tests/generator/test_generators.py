import random
from typing import Any
from unittest.mock import patch

import pytest

from generator.generators import generator_Adam
from generator.grid import Grid


# checks if all area is filled
# and solution is found (TODO: implement pathfinding, possibly from a package?)
def test_generator_Adam(capfd: pytest.CaptureFixture[str]) -> None:
    maze = generator_Adam(10, 10, (2, 3), (5, 7), stop_coeff=100)
    grid = Grid(maze)
    grid.__debug_print__()
    out, err = capfd.readouterr()
    assert out.find("█") == -1


def test_random_mocking_basic() -> None:
    with patch("random.choices", side_effect=lambda x: [x[1]]):
        assert random.choices([1, 2, 3])[0] == 2


# neede for the next test
# to avoid recursion, i preserve the original function under a different name
values = 0
temp_random_choices = random.choices


# test if i can fake first 10 values
def test_random_mocking_advanced() -> None:
    def mock_random_choices(*args: Any) -> list[int]:
        global values
        if values < 10:
            values += 1
            return [0]
        return temp_random_choices(*args)

    with patch(
        "random.choices",
        side_effect=lambda *args: mock_random_choices(*args),
    ):
        for i in range(10):
            assert random.choices([1, 2, 3])[0] == 0
        temp_value = random.choices([1, 2, 3])[0]
        assert temp_value == 1 or temp_value == 2 or temp_value == 3


# reset of the value
values = 0


# checks if upon dead end a new solution can be found
def test_generator_Adam_dead_end_solution(capfd: pytest.CaptureFixture[str]) -> None:
    # local function for choosing random variable
    def mock_random_choices(*args: Any) -> list[tuple[int, int]]:
        global values
        direction_list = [(0, 1), (1, 1), (2, 1), (2, 0), (1, 0)]
        if values < len(direction_list):
            values += 1
            return [direction_list[values]]
        return temp_random_choices(*args)

    # actual lairynth testing
    with patch(
        "random.choices",
        side_effect=lambda *args: mock_random_choices(*args),
    ):
        maze = generator_Adam(5, 2, (0, 0), (4, 1), towards_coeff=100)
        grid = Grid(maze)
        grid.__debug_print__()
        out, err = capfd.readouterr()
        assert out.find("█") == -1
