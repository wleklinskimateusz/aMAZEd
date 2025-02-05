from collections import defaultdict
from operator import itemgetter


class Maze:
    """A class that represents a maze as a graph."""

    def __init__(self) -> None:
        self.graph: defaultdict[tuple[int, int], set[tuple[int, int]]] = defaultdict(
            set
        )

    def add_connection(self, cell1: tuple[int, int], cell2: tuple[int, int]) -> None:
        """Adds a connection only if it's visually possible."""
        if self.__are_adjacent(cell1, cell2):
            self.graph[cell1].add(cell2)
            self.graph[cell2].add(cell1)
        else:
            raise ValueError(f"Invalid connection: {cell1} ↔ {cell2}")

    def __are_adjacent(self, cell1: tuple[int, int], cell2: tuple[int, int]) -> bool:
        """Checks if two cells are directly adjacent in a grid structure."""
        r1, c1 = cell1
        r2, c2 = cell2
        return (abs(r1 - r2) == 1 and c1 == c2) or (abs(c1 - c2) == 1 and r1 == r2)

    def is_connected(self, cell1: tuple[int, int], cell2: tuple[int, int]) -> bool:
        """Checks if two cells are connected."""
        return cell2 in self.graph[cell1]

    def get_connections(self, cell: tuple[int, int]) -> set[tuple[int, int]]:
        """Returns all connected neighbors."""
        return self.graph[cell]

    def size(self) -> tuple[int, int]:
        """Returns tuple of maze dimensions (rows, columns)"""
        templist = list(self.graph.keys())
        return max(templist, key=itemgetter(0))[0] + 1, max(
            templist, key=itemgetter(1)
        )[1] + 1
