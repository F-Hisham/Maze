import copy
import random
import math
from typing import Tuple
from collections import OrderedDict

from maze.cells import Coords, Moves

from solvers.base import BaseMazeSolver


class SimpleMazeSolver(BaseMazeSolver):
    def solve(self):
        path, found = self.snake_path_recursive(path=(self.start_coords,))
        final_path = copy.deepcopy(self.original_maze)
        final_path.apply_path(path)
        final_path.plot()
        return path if found else ()

    # Option 1: Simply prioritizes the down, right path
    # def roads_priority(self, path, all_new_coords)->Tuple[Tuple[Coords]]:
    #     roadsmap = {}
    #     for coords in all_new_coords:
    #         # Mapping not good in cells.py file
    #         # Better to add __sub__ (return Coords(self.x - other.x, self.y - other.y)) in cells.py file instead of doing as below
    #         # if Coords(coords.x - path[-1].x, coords.y - path[-1].y) == Moves.RIGHT: roadsmap["aDOWN"] = coords
    #         # if Coords(coords.x - path[-1].x, coords.y - path[-1].y) == Moves.DOWN: roadsmap["bRIGHT"] = coords
    #         # if Coords(coords.x - path[-1].x, coords.y - path[-1].y) == Moves.LEFT: roadsmap["cUP"] = coords
    #         # if Coords(coords.x - path[-1].x, coords.y - path[-1].y) == Moves.UP: roadsmap["dLEFT"] = coords
    #     return list(OrderedDict(sorted(roadsmap.items())).values())

    # Option 2: More dynamic than option one as it considers the end coordinates and the current position to determine the best next move to prioritize
    def roads_priority(self, path, all_new_coords) -> Tuple[Tuple[Coords], bool]:
        best_move = self.best_next_move_knowing_end(path)
        roadsmap = self.roads_mapping(path, all_new_coords)

        for k in best_move:
            if k not in roadsmap.keys(): best_move.remove(k)
        for k in best_move:
            if k not in roadsmap.keys(): best_move.remove(k)

        all_new_coords = list()
        if len(best_move)==1:
            all_new_coords.append(roadsmap[best_move[0]])
        elif len(best_move)>1:
            all_new_coords.append(roadsmap[best_move[0]])
            all_new_coords.append(roadsmap[best_move[1]])
        for k2 in best_move:
            roadsmap.pop(k2)

        for k3 in roadsmap.keys():
            all_new_coords.append(roadsmap[k3])

        return tuple(all_new_coords)

    def roads_mapping(self, path, all_new_coords):
        roadsmap = {}
        for coords in all_new_coords:
            # Mapping not good in cells.py file
            # Better to add __sub__ (return Coords(self.x - other.x, self.y - other.y)) in cells.py file instead of doing as below
            if Coords(coords.x - path[-1].x, coords.y - path[-1].y) == Moves.RIGHT: roadsmap["D"] = coords
            if Coords(coords.x - path[-1].x, coords.y - path[-1].y) == Moves.DOWN: roadsmap["R"] = coords
            if Coords(coords.x - path[-1].x, coords.y - path[-1].y) == Moves.LEFT: roadsmap["U"] = coords
            if Coords(coords.x - path[-1].x, coords.y - path[-1].y) == Moves.UP: roadsmap["L"] = coords
        return roadsmap

    def best_next_move_knowing_end(self, path):
        startpoint_endpoint_distance = Coords(self.end_coords.x - path[-1].x, self.end_coords.y - path[-1].y)
        if (self.end_coords.x - path[-1].x) != 0:
            slope = (self.end_coords.y - path[-1].y) / (self.end_coords.x - path[-1].x)  # can add this in cells.py
        else:
            slope = 0.01

        if startpoint_endpoint_distance.x >= 0 and startpoint_endpoint_distance.y >= 0:  # Right and Down
            if -1 < slope < 1:  # prioritize left or right
                return ["R", "D"]
            else:
                return ["D", "R"]
        if startpoint_endpoint_distance.x > 0 and startpoint_endpoint_distance.y < 0:  # Right and Up
            if -1 < slope < 1:  # prioritize left or right
                return ["R", "U"]
            else:
                return ["U", "R"]
        if startpoint_endpoint_distance.x < 0 and startpoint_endpoint_distance.y > 0:  # Left and Down
            if -1 < slope < 1:  # prioritize left or right
                return ["L", "D"]
            else:
                return ["D", "L"]
        if startpoint_endpoint_distance.x < 0 and startpoint_endpoint_distance.y < 0:  # Left and Up
            if -1 < slope < 1:  # prioritize left or right
                return ["L", "U"]
            else:
                return ["U", "L"]

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
                if len(all_new_coords) > 1:
                    all_new_coords = self.roads_priority(path, all_new_coords)

                # random.shuffle(all_new_coords)
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
        return math.sqrt((cb.x - ca.x) ** 2 + (cb.y - ca.y) ** 2)
