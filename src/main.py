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


if __name__ == "__main__":
    main()
