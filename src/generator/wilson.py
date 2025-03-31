from random import randint

from generator.generator import Generator


class Wilson(Generator):
    """A class for generating a maze using the Wilson algorithm"""

    def __init__(self, height: int = 10, width: int = 10) -> None:
        if height < 2 or width < 2:
            raise ValueError("Invalid maze size, must be at least 2x2")

        Generator.__init__(height, width)
        self.unconnected = [
            (
                iter // self.width,
                iter % self.width,
            )
            for iter in range(int(self.height * self.width))
        ]

        self.unconnected.remove(
            (randint(0, self.height - 1), randint(0, self.width - 1))
        )
        while not self.add_branch():
            pass

    def step(self) -> None:
        while True:
            temp = randint(0, 3)
            proposed_expansion = (
                self.branch[-1][0] + (2 * (temp % 2) - 1) * (temp // 2 - 1),
                self.branch[-1][1] + (2 * (temp % 2) - 1) * (temp // 2),
            )
            if (
                (
                    (len(self.branch) > 1 and proposed_expansion != self.branch[-2])
                    or len(self.branch) < 2
                )
                and proposed_expansion[0] in range(self.height)
                and proposed_expansion[1] in range(self.width)
            ):
                break
        if proposed_expansion in self.branch:
            self.branch.pop()
            self.branch.pop()
            self.branch.pop()
        else:
            self.branch.append(proposed_expansion)

    def add_branch(self) -> int:
        """Adds a new branch to the maze if possible"""
        if len(self.unconnected) == 0:
            return -1

        self.branch = [self.unconnected[randint(0, len(self.unconnected) - 1)]]

        while self.branch[-1] in self.unconnected:
            self.step()

        for iter in range(len(self.branch) - 1):
            self.maze.add_connection(self.branch[iter], self.branch[iter + 1])
            self.unconnected.remove(self.branch[iter])

        self.branch = []

        return 0
