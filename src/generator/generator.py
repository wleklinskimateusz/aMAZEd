from abc import ABC, abstractmethod

from generator.maze import Maze


class Generator(ABC):
    def __init__(
        self,
        height: int,
        width: int,
        start: tuple[int, int],
        end: tuple[int, int],
    ) -> None:
        """Initialize the generator with maze parameters.

        Args:
            height: Height of the maze
            width: Width of the maze
            start: Starting point coordinates (x, y)
            end: End point coordinates (x, y)
        """
        self.height = height
        self.width = width
        self.start = start
        self.end = end

    @abstractmethod
    def generate(self) -> Maze:
        pass
