import copy
import random
import math
from typing import Tuple

from maze.cells import Coords, Moves

from solvers.base import BaseMazeSolver


class SimpleMazeSolver(BaseMazeSolver):
    def solve(self):
        path, found = self.snake_path_recursive(path=(self.start_coords,))
        final_path = copy.deepcopy(self.original_maze)
        final_path.apply_path(path)
        final_path.plot()
        return path if found else ()

    def snake_path_recursive(
        self, path: Tuple[Coords], found: bool = False
    ) -> Tuple[Tuple[Coords], bool]:

        if found:
            return path, found

        pre_maze = copy.deepcopy(self.original_maze)
        pre_maze.apply_path(path[:-1])

        if pre_maze.is_valid_road(path[-1]):

            post_maze = copy.deepcopy(pre_maze)
            post_maze.apply_path((path[-1],))
            if self.visualize:
                post_maze.plot()

            if path[-1] == self.end_coords:
                return path, True
            else:
                all_new_coords = list(post_maze.adjacent_roads(path[-1]))
                random.shuffle(all_new_coords)
                for new_coords in all_new_coords:
                    new_path = path + (new_coords,)
                    new_path, new_found = self.snake_path_recursive(path=new_path)  # type: ignore
                    if new_found:
                        return new_path, new_found

        return path, False

    @staticmethod
    def move_coords(coords, move):
        return Coords(coords.x + move[0], coords.y + move[1])


class PseudoDirectionalMazeSolver(BaseMazeSolver):
    def solve(self):
        path, found = self.snake_path_recursive(path=(self.start_coords,))
        final_path = copy.deepcopy(self.original_maze)
        final_path.apply_path(path)
        final_path.plot()
        return path if found else ()

    def snake_path_recursive(
        self, path: Tuple[Coords], found: bool = False
    ) -> Tuple[Tuple[Coords], bool]:

        if found:
            return path, found

        pre_maze = copy.deepcopy(self.original_maze)
        pre_maze.apply_path(path[:-1])

        if pre_maze.is_valid_road(path[-1]):

            post_maze = copy.deepcopy(pre_maze)
            post_maze.apply_path((path[-1],))
            if self.visualize:
                post_maze.plot()

            if path[-1] == self.end_coords:
                return path, True
            else:
                all_new_coords = list(post_maze.adjacent_roads(path[-1]))
                coords_and_distance = [
                    (c, self.distance(self.end_coords, c)) for c in all_new_coords
                ]
                coords_and_distance = sorted(coords_and_distance, key=lambda x: x[1])
                for new_coords, _ in coords_and_distance:
                    new_path = path + (new_coords,)
                    new_path, new_found = self.snake_path_recursive(path=new_path)  # type: ignore
                    if new_found:
                        return new_path, new_found

        return path, False

    @staticmethod
    def distance(ca, cb):
        return math.sqrt((cb.x-ca.x)**2 + (cb.y-ca.y)**2)
