from generator.generators import generator_Adam
from generator.grid import Grid
from generator.maze import Maze


def main() -> None:
    maze = Maze()
    print("[INFO] Empty maze created")

    maze.add_connection((0, 0), (0, 1))
    print("[INFO] Connection added: (0, 0) ↔ (0, 1)")

    maze.add_connection((0, 1), (0, 2))
    print("[INFO] Connection added: (0, 1) ↔ (0, 2)")

    maze.add_connection((0, 2), (1, 2))
    print("[INFO] Connection added: (0, 2) ↔ (1, 2)")

    maze.add_connection((0, 2), (0, 3))
    print("[INFO] Connection added: (0, 2) ↔ (0, 3)")

    print("[INFO] All connections for (0, 2) node: ", maze.get_connections((0, 2)))

    print("Size of the maze: ", maze.size())

    grid = Grid(maze)
    print("Crude maze representation:")
    grid.__debug_print__()
    print("")

    generated_maze = generator_Adam(10, 10, (0, 0), (9, 9))
    generated_grid = Grid(generated_maze)
    print("Crude generated maze representation (start (0,0), end (9,9)):")
    generated_grid.__debug_print__()


if __name__ == "__main__":
    main()
