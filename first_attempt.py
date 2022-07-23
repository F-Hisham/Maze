import copy
import enum
import random
from dataclasses import dataclass
from typing import List, Tuple

import matplotlib
from matplotlib import pyplot as plt

plt.ion()
MAZE_PLOT, MAZE_AXIS = plt.subplots()


@dataclass
class Coords:
    x: int
    y: int

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


class Locations(enum.Enum):

    ROAD = 0
    BLOCK = 1
    PATH = 2


class Maze:

    def __init__(self, array, road_symbol=Locations.ROAD, block_symbol=Locations.BLOCK):
        self.maze = self.sanitize_maze(array, road_symbol, block_symbol)

    @staticmethod
    def sanitize_maze(maze, road_symbol=Locations.ROAD, block_symbol=Locations.BLOCK):

        def sanitized_symbol(symbol_in):
            if Locations(symbol_in) == road_symbol:
                return Locations.ROAD.value
            elif Locations(symbol_in) == block_symbol:
                return Locations.BLOCK.value
            else:
                raise RuntimeError(f"Cannot parse symbol {symbol_in}")

        sanitized_maze = [[sanitized_symbol(x) for x in row] for row in maze]
        return sanitized_maze

    @property
    def rows(self):
        return len(self.maze)

    @property
    def cols(self):
        lengths = [len(x) for x in self.maze]
        orig_len = lengths[0]
        equal_lengths = all([length - orig_len == 0 for length in lengths])
        if equal_lengths:
            return orig_len
        else:
            raise RuntimeError(f"Not all rows have the same number of cols.")

    def __repr__(self):
        header_indices = list(range(0, self.cols))
        header = f"Idx |{header_indices}"
        separation = "_" * len(header)
        formatted_rows = []

        for i, row in enumerate(self.maze):
            formatted_rows.append(f" {i}  |{row}")

        output = "\n".join([header, separation, *formatted_rows])
        return output + "\n"

    def value(self, coords: Coords) -> Locations:
        return Locations(self.maze[coords.y][coords.x])

    def set_value(self, coords: Coords, val):
        self.maze[coords.y][coords.x] = Locations(val).value

    def is_valid_road(self, coords):
        if 0 <= coords.x < self.cols and 0 <= coords.y < self.rows:
            return self.value(coords) == Locations.ROAD
        else:
            return False

    def apply_path(self, path):
        for coords in path:
            if self.is_valid_road(coords):
                self.set_value(coords, val=Locations.PATH)
            else:
                raise RuntimeError(f"Coords {coords} are not a valid road.")

    def plot(self):
        MAZE_AXIS.clear()
        im = MAZE_AXIS.imshow(self.maze)
        #plt.show()
        plt.pause(interval=0.01)      # type: ignore
        

class MazeSolver:
    UP = (0, 1)
    DOWN = (0, -1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)
    MOVES = [UP, DOWN, LEFT, RIGHT]

    def __init__(self, maze: Maze, start_coords: Coords, end_coords: Coords):
        self.original_maze = maze
        self.path_maze = copy.deepcopy(maze)
        self.start_coords = start_coords
        self.end_coords = end_coords

    def is_path(self):
        self.path_maze.set_value(self.start_coords, val=Locations.PATH)
        last_coords = [self.start_coords]

        while self.path_maze.value(self.end_coords) != Locations.PATH:
            new_coords = []

            for coords in last_coords:
                for move in self.MOVES:
                    new_single = self.move_coords(coords, move=move)
                    if self.path_maze.is_valid_road(new_single):
                        new_coords.append(new_single)

            if new_coords:
                for coords in new_coords:
                    self.path_maze.set_value(coords=coords, val=Locations.PATH)
            else:
                return False

            last_coords = new_coords
            print(self.path_maze)

        return True

    def snake_path(self):
        path, found = self.snake_path_recursive(path=(self.start_coords,))
        return path

    def snake_path_recursive(self, path: Tuple[Coords], found: bool = False) -> Tuple[Tuple[Coords], bool]:

        if found:
            return path, found

        pre_maze = copy.deepcopy(self.original_maze)
        pre_maze.apply_path(path[:-1])

        if pre_maze.is_valid_road(path[-1]):

            post_maze = copy.deepcopy(pre_maze)
            post_maze.apply_path((path[-1],))
            post_maze.plot()

            if path[-1] == self.end_coords:
                return path, True
            else:
                all_new_coords = [
                    self.move_coords(path[-1], move) for move in self.MOVES
                ]
                random.shuffle(all_new_coords)
                for new_coords in all_new_coords:
                    new_path = path + (new_coords,)
                    new_path, new_found = self.snake_path_recursive(path=new_path)
                    if new_found:
                        return new_path, new_found

        return path, False

    @staticmethod
    def move_coords(coords, move):
        return Coords(coords.x + move[0], coords.y + move[1])


def main():
    maze = Maze(array=[
        [0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
        [1, 1, 1, 1, 0, 1, 0, 0, 0, 1],
        [0, 0, 0, 1, 0, 1, 1, 1, 0, 1],
        [0, 0, 0, 1, 0, 0, 1, 0, 0, 1],
        [0, 0, 0, 1, 1, 0, 1, 0, 1, 1],
        [0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
        [0, 1, 1, 1, 1, 1, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 1, 0, 1, 1, 0, 0],
        [0, 1, 0, 0, 1, 0, 1, 0, 0, 0],
    ])

    start = Coords(x=0, y=0)
    end = Coords(x=9, y=9)

    maze_solver = MazeSolver(maze, start, end)
    output = maze_solver.snake_path()
    print(output)
    temp = 1


if __name__ == "__main__":
    main()
