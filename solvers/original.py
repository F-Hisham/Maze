import copy
import random
from typing import Tuple
from maze.maze import Maze
from maze.cells import Coords
from maze.constants import Locations


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
