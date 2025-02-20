import random

from generator.maze import Maze


def generator_Adam(
    width: int, height: int, start: tuple[int, int], end: tuple[int, int]
) -> Maze:
    # coefficients
    # solution
    towards_coeff = 2.0
    elsewhere_coeff = 1.0
    # branching
    stop_coeff = 10000
    turn_coeff = 1.0

    # function for adding and subtracting tuples
    def add(t1: tuple[int, int], t2: tuple[int, int]) -> tuple[int, int]:
        return t1[0] + t2[0], t1[1] + t2[1]

    # init
    internal_maze = Maze()
    solution = [start]
    used_places = [start]

    # a loop that makes sure a good solution will be found
    while solution[-1] != end:
        internal_maze = Maze()
        solution = [start]
        used_places = [start]
        # a loop that searches for a solution
        while solution[-1] != end:
            direction = (end[0] - solution[-1][0], end[1] - solution[-1][1])
            weights = []
            connections = []
            # checks if the tile is inside the maze and not used before (connections==0)
            # and then adds option with a weight dependant if its toward or not the end
            # right
            if (
                solution[-1][0] + 1 <= end[0]
                and len(internal_maze.get_connections(add(solution[-1], (1, 0)))) == 0
            ):
                weights += [
                    elsewhere_coeff
                    + (towards_coeff - elsewhere_coeff) * float(direction[0] >= 0.0)
                ]
                connections += [add(solution[-1], (1, 0))]
            # left
            if (
                solution[-1][0] - 1 >= 0
                and len(internal_maze.get_connections(add(solution[-1], (-1, 0)))) == 0
            ):
                weights += [
                    elsewhere_coeff
                    + (towards_coeff - elsewhere_coeff) * float(direction[0] <= 0.0)
                ]
                connections += [add(solution[-1], (-1, 0))]
            # up
            if (
                solution[-1][1] + 1 <= end[1]
                and len(internal_maze.get_connections(add(solution[-1], (0, 1)))) == 0
            ):
                weights += [
                    elsewhere_coeff
                    + (towards_coeff - elsewhere_coeff) * float(direction[1] >= 0.0)
                ]
                connections += [add(solution[-1], (0, 1))]
            # down
            if (
                solution[-1][1] - 1 >= 0
                and len(internal_maze.get_connections(add(solution[-1], (0, -1)))) == 0
            ):
                weights += [
                    elsewhere_coeff
                    + (towards_coeff - elsewhere_coeff) * float(direction[1] <= 0.0)
                ]
                connections += [add(solution[-1], (0, -1))]
            # that means there is a dead end in a solution
            if len(weights) == 0:
                break
            # choosing the next tile
            next_tile = random.choices(connections, weights)[0]
            solution += [next_tile]
            used_places += [next_tile]
            internal_maze.add_connection(solution[-2], solution[-1])
        # end of a search loop
    # end of a solution loop

    # loop that branches from all used places if possible
    i = -1
    while i < len(used_places) - 1:
        i += 1
        print(str(i) + ", " + str(len(used_places)))
        # checks if can branch from this tile
        if len(internal_maze.get_connections(used_places[i])) == 4:
            continue
        # branches and adds all tiles onto "used_places"
        while True:
            weights = []
            connections = []
            # checks if the tile is inside the maze and not used before (connections==0)
            # and then adds option with a weight dependant if its toward or not the end
            # right
            if (
                used_places[i][0] + 1 <= end[0]
                and len(internal_maze.get_connections(add(used_places[i], (1, 0)))) == 0
            ):
                weights += [1.0]
                connections += [add(used_places[i], (1, 0))]
            # left
            if (
                used_places[i][0] - 1 >= 0
                and len(internal_maze.get_connections(add(used_places[i], (-1, 0))))
                == 0
            ):
                weights += [1.0]
                connections += [add(used_places[i], (-1, 0))]
            # up
            if (
                used_places[i][1] + 1 <= end[1]
                and len(internal_maze.get_connections(add(used_places[i], (0, 1)))) == 0
            ):
                weights += [1.0]
                connections += [add(used_places[i], (0, 1))]
            # down
            if (
                used_places[i][1] - 1 >= 0
                and len(internal_maze.get_connections(add(used_places[i], (0, -1))))
                == 0
            ):
                weights += [1.0]
                connections += [add(used_places[i], (0, -1))]
            # when next connection would make a straight line, it favours turning
            # by making perpendicular weights bigger
            temp_connections = list(internal_maze.get_connections(used_places[i]))
            if len(temp_connections) == 1 and len(connections) != 1:
                # up/down movement adds weight to right/left
                if temp_connections[0][1] - used_places[i][1] == 0:
                    for j in range(len(connections)):
                        if connections[j][0] - used_places[i][0] == 0:
                            weights[j] += turn_coeff
                # right/left movement adds weight to up/down
                if temp_connections[0][0] - used_places[i][0] == 0:
                    for j in range(len(connections)):
                        if connections[j][1] - used_places[i][1] == 0:
                            weights[j] += turn_coeff
            # stop option
            weights += [stop_coeff]
            connections += [(-1, -1)]
            # choosing the next tile
            next_tile = random.choices(connections, weights)[0]
            if next_tile[0] < 0:
                break
            used_places += [next_tile]
            internal_maze.add_connection(used_places[i], next_tile)
        # checks if whole labirynth has been filled
        if len(used_places) == width * height:
            break
    # end of branching loop

    return internal_maze
