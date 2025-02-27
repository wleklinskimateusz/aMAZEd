import random

from generator.maze import Maze


# function for adding and subtracting tuples
def __add__(t1: tuple[int, int], t2: tuple[int, int]) -> tuple[int, int]:
    return t1[0] + t2[0], t1[1] + t2[1]


# returns connections and weights for choosing a random connection
# when weight 0 it means it is not eligible to choose
# order: right, left, up, down
def __connections_and_weights__(
    init_maze: Maze,
    width: int,
    height: int,
    position: tuple[int, int],
    init_weight: float,
) -> tuple[list[float], list[tuple[int, int]]]:
    weights = [0.0, 0.0, 0.0, 0.0]
    connections = []
    # right
    if (
        position[0] + 1 < width
        and len(init_maze.get_connections(__add__(position, (1, 0)))) == 0
    ):
        weights[0] += init_weight
    connections += [__add__(position, (1, 0))]
    # left
    if (
        position[0] - 1 >= 0
        and len(init_maze.get_connections(__add__(position, (-1, 0)))) == 0
    ):
        weights[1] += init_weight
    connections += [__add__(position, (-1, 0))]
    # up
    if (
        position[1] + 1 < height
        and len(init_maze.get_connections(__add__(position, (0, 1)))) == 0
    ):
        weights[2] += init_weight
    connections += [__add__(position, (0, 1))]
    # down
    if (
        position[1] - 1 >= 0
        and len(init_maze.get_connections(__add__(position, (0, -1)))) == 0
    ):
        weights[3] += init_weight
    connections += [__add__(position, (0, -1))]
    return weights, connections


# function to correct weights when searching for a solution
# because we might want to go more towards a solution (correction>0)
# or meander a bit (correction<0)
def __weight_correction_for_solution__(
    init_weights: list[float],
    position: tuple[int, int],
    end: tuple[int, int],
    correction: float,
) -> list[float]:
    corrected_weights = init_weights
    direction = (end[0] - position[0], end[1] - position[1])
    # correction order: right, left, up, down
    corrected_weights[0] += correction * float(
        direction[0] >= 0.0 and corrected_weights[0] != 0
    )
    corrected_weights[1] += correction * float(
        direction[0] <= 0.0 and corrected_weights[1] != 0
    )
    corrected_weights[2] += correction * float(
        direction[1] >= 0.0 and corrected_weights[2] != 0
    )
    corrected_weights[3] += correction * float(
        direction[1] <= 0.0 and corrected_weights[3] != 0
    )
    return corrected_weights


# if we want branching to switch directions more, we need to
# assign bigger weights to branches perpendicular to current direction
def __weight_correction_for_direction__(
    init_maze: Maze,
    init_weights: list[float],
    position: tuple[int, int],
    correction: float,
) -> list[float]:
    corrected_weights = init_weights
    temp_connections = list(init_maze.get_connections(position))
    # checking if currently checked tile is at the end of a branch (1 connection)
    # and if it *can* turn in any way
    if len(temp_connections) == 1 and sum([w != 0 for w in corrected_weights]) > 1:
        # order: right, left, up, down
        # up/down movement adds weight to right/left
        if temp_connections[0][1] - position[1] != 0:
            if corrected_weights[0] != 0:
                corrected_weights[0] += correction
            if corrected_weights[1] != 0:
                corrected_weights[1] += correction
        # right/left movement adds weight to up/down
        if temp_connections[0][0] - position[0] != 0:
            if corrected_weights[2] != 0:
                corrected_weights[2] += correction
            if corrected_weights[3] != 0:
                corrected_weights[3] += correction
    return corrected_weights


def generator_Adam(
    width: int,
    height: int,
    start: tuple[int, int],
    end: tuple[int, int],
    towards_coeff: float = 2.0,
    elsewhere_coeff: float = 1.0,
    stop_coeff: float = 0.2,
    turn_coeff: float = 1.0,
) -> Maze:
    # coefficients:
    #   solution:
    #     towards_coeff = 2.0
    #     elsewhere_coeff = 1.0
    #   branching:
    #     stop_coeff = 0.2  # when set too high, a nigh-infinite loop is possible
    #     turn_coeff = 1.0

    # check if start and end are inside the maze
    if start[0] < 0 or start[0] >= width or start[1] < 0 or start[1] >= height:
        raise ValueError("Invalid start position; outside the maze")
    if end[0] < 0 or end[0] >= width or end[1] < 0 or end[1] >= height:
        raise ValueError("Invalid end position; outside the maze")
    # check if start and end are different tiles
    if start[0] == end[0] and start[1] == end[1]:
        raise ValueError("Invalid start/end position; they shouldn't be equal")

    solution = [start]
    # a loop that makes sure a good solution will be found
    # because sometimes solution search fails
    # then it is restarted
    while solution[-1] != end:
        internal_maze = Maze()
        solution = [start]
        used_places = [start]
        # a loop that searches for a solution
        while solution[-1] != end:
            # checks where we can go from current last tile of a solution
            weights, connections = __connections_and_weights__(
                internal_maze, width, height, solution[-1], elsewhere_coeff
            )
            # adds value to the weights in direction of the end
            weights = __weight_correction_for_solution__(
                weights, solution[-1], end, towards_coeff - elsewhere_coeff
            )
            # that means there is a dead end in a solution
            # none of them have a positive weights, so none can get choosen
            if sum(weights) == 0:
                break
            # choosing the next tile
            next_tile = random.choices(connections, weights)[0]
            solution += [next_tile]
            used_places += [next_tile]
            internal_maze.add_connection(solution[-2], solution[-1])
        # end of a search loop
    # end of a solution loop

    # loop that branches from all used places if possible
    # stops if all places in a labirynth were checked
    i = -1
    while i < len(used_places) - 1:
        i += 1
        # checks if can branch from this tile
        if len(internal_maze.get_connections(used_places[i])) == 4:
            continue
        # branches and adds all tiles onto "used_places"
        while True:
            # checks where we can go from current last checked used tile
            weights, connections = __connections_and_weights__(
                internal_maze, width, height, used_places[i], 1.0
            )
            # when next connection would make a straight line, it favours turning
            # by making perpendicular weights bigger
            weights = __weight_correction_for_direction__(
                internal_maze, weights, used_places[i], turn_coeff
            )
            # adding stop option to end the branching
            weights += [stop_coeff]
            connections += [(-1, -1)]
            # choosing the next tile
            next_tile = random.choices(connections, weights)[0]
            if next_tile[0] < 0:
                break
            used_places += [next_tile]
            internal_maze.add_connection(used_places[i], next_tile)
        # end of branching loop

        # checks if whole labirynth has been filled
        # if not, starts from the beginning again
        if i == len(used_places) - 1 and len(used_places) != width * height:
            i = -1
    # end of checking loop

    return internal_maze
