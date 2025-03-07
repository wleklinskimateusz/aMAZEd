from collections import defaultdict
from generator.maze import Maze
from random import randint


class Wilson(Maze):
    """A class for generating a maze using the Wilson algorithm"""

    def __init__(self, maze_size: tuple[int, int] = (10, 10)) -> None:
        if maze_size[0] < 2 or maze_size[1] < 2:
            raise ValueError("Invalid maze size, must be at least 2x2")
        self.graph: defaultdict[tuple[int, int], set[tuple[int, int]]] = defaultdict(
            set
        )
        self.maze_size = maze_size
        self.unconnected = [
            (
                iter // self.maze_size[1],
                iter % self.maze_size[1],
            )
            for iter in range(int(self.maze_size[0] * self.maze_size[1]))
        ]

        self.unconnected.remove(
            (randint(0, self.maze_size[0] - 1), randint(0, self.maze_size[1] - 1))
        )
        while not self.Add_Branch():
            pass

    def Add_Branch(self) -> int:
        """Adds a new branch to the maze if possible"""
        if len(self.unconnected) == 0:
            return -1

        branch = [self.unconnected[randint(0, len(self.unconnected) - 1)]]

        while branch[-1] in self.unconnected:
            temp = randint(0, 3)
            proposed_expansion = (
                branch[-1][0] + (2 * (temp % 2) - 1) * (temp // 2 - 1),
                branch[-1][1] + (2 * (temp % 2) - 1) * (temp // 2),
            )

            if (
                proposed_expansion[0] not in range(self.maze_size[0])
                or proposed_expansion[1] not in range(self.maze_size[1])
                or len(branch) > 1
                and proposed_expansion == branch[-2]
            ):
                continue
            elif proposed_expansion in branch:
                branch.pop()
                branch.pop()
                branch.pop()
            else:
                branch.append(proposed_expansion)

        for iter in range(len(branch) - 1):
            self.add_connection(branch[iter], branch[iter + 1])
            self.unconnected.remove(branch[iter])

        return 0
