from generator.maze import Maze


class Grid:
    """A class to transform a maze into a printable grid"""

    def __init__(self, input: Maze) -> None:
        # creating grid
        rows, cols = input.size()
        self.grid = [[0 for i in range(cols)] for j in range(rows)]
        if rows == 0 or cols == 0:
            return
        for k in input.graph.keys():
            connections = input.get_connections(k)
            if len(connections) == 0:
                continue
            for c in connections:
                # up    = 2^0
                if c[0] > k[0]:
                    self.grid[k[0]][k[1]] += 1
                # right = 2^1
                elif c[1] > k[1]:
                    self.grid[k[0]][k[1]] += 2
                # down  = 2^2
                elif c[0] < k[0]:
                    self.grid[k[0]][k[1]] += 4
                # left = 2^3
                elif c[1] < k[1]:
                    self.grid[k[0]][k[1]] += 8

    def __debug_print__(self) -> None:
        tempdict = {
            0: "█",
            1: "╨",
            2: "╞",
            3: "╚",
            4: "╥",
            5: "║",
            6: "╔",
            7: "╠",
            8: "╡",
            9: "╝",
            10: "═",
            11: "╩",
            12: "╗",
            13: "╣",
            14: "╦",
            15: "╬",
        }
        gridcopy = self.grid[:]
        gridcopy.reverse()
        for row in gridcopy:
            for space in row:
                print(tempdict[space], sep="", end="")
            print("")
