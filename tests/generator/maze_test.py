import pytest

from generator.grid import Grid
from generator.maze import Maze


def test_empty_maze() -> None:
    maze = Maze()
    assert maze.graph == {}


def test_add_connection() -> None:
    maze = Maze()
    maze.add_connection((0, 0), (0, 1))
    assert maze.is_connected((0, 0), (0, 1))
    assert maze.is_connected((0, 1), (0, 0))
    assert maze.get_connections((0, 0)) == {(0, 1)}
    assert maze.get_connections((0, 1)) == {(0, 0)}


def test_invalid_connection() -> None:
    maze = Maze()
    with pytest.raises(ValueError):
        maze.add_connection((0, 0), (1, 1))
    assert maze.get_connections((0, 0)) == set()
    assert maze.get_connections((1, 1)) == set()


def test_keep_adding_connections() -> None:
    maze = Maze()
    maze.add_connection((0, 0), (0, 1))
    maze.add_connection((0, 1), (0, 2))
    maze.add_connection((0, 2), (0, 3))
    assert maze.is_connected((0, 0), (0, 1))
    assert maze.is_connected((0, 1), (0, 2))
    assert maze.is_connected((0, 2), (0, 3))

    node = (0, 3)
    new_connection = next(iter(maze.get_connections(node)))
    assert new_connection == (0, 2)


def test_size_check() -> None:
    maze = Maze()
    maze.add_connection((0, 0), (0, 1))
    maze.add_connection((0, 1), (0, 2))
    maze.add_connection((0, 2), (0, 3))
    assert maze.size() == (1, 4)
    maze.add_connection((0, 1), (1, 1))
    assert maze.size() == (2, 4)


def test_grid_creation() -> None:
    maze = Maze()
    grid = Grid(maze)
    assert grid.grid == []


def test_crude_grid_drawing(capfd: pytest.CaptureFixture[str]) -> None:
    maze = Maze()
    maze.add_connection((0, 0), (0, 1))
    maze.add_connection((0, 1), (0, 2))
    maze.add_connection((0, 2), (0, 3))
    maze.add_connection((0, 1), (1, 1))
    grid = Grid(maze)
    grid.__debug_print__()
    out, err = capfd.readouterr()
    assert out == "█╥██\n╞╩═╡\n"
