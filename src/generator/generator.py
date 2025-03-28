from abc import ABC, abstractmethod

from generator.maze import Maze


class Generator(ABC):
    def __init__(
        self,
        height: int,
        width: int,
    ) -> None:
        """Initialize the generator with maze parameters.

        Args:
            height: Height of the maze
            width: Width of the maze
        """
        self.height = height
        self.width = width
        self.maze = Maze()

    @abstractmethod
    def generate(self) -> None:
        """Generate the maze. save it to self.maze"""
        pass
