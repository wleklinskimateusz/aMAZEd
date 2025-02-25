import pytest

from generator.wilson import Wilson
from generator.grid import Grid
from generator.maze import Maze


def test_invalid_size() -> None:
    # test if it catches an improperly set maze_size
    maze = Maze()
    with pytest.raises(ValueError):
        maze = Wilson((0,0))
    assert maze.get_connections((0, 0)) == set()



def test_maze_completness(capfd: pytest.CaptureFixture[str]) -> None:
    # checks if all area is filled
    maze = Wilson()
    grid = Grid(maze)
    grid.__debug_print__()
    out, err = capfd.readouterr()
    assert out.find("█") == -1


