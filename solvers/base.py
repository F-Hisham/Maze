import time
from abc import ABC, abstractmethod
from typing import Tuple

from maze.cells import Coords
from maze.basic_maze import Maze


class BaseMazeSolver(ABC):
    def __init__(
        self,
        maze: Maze,
        start_coords: Coords,
        end_coords: Coords,
        visualize: bool = False,
    ):
        # Do not attempt to modify original maze, it is needed for validation
        self.__original_maze = maze
        
        # Do not modify the start and end coordinates either
        self.start_coords = start_coords
        self.end_coords = end_coords
        
        # If you have any plotting, make sure it can be turned on and off using 
        # the visualize attribute below
        self.visualize = visualize
        
        # If you have any random number generators, use this for the
        # seed to allow for testing with different random number series
        self.rand_seed = 1

    @property
    def original_maze(self):
        return self.__original_maze
    
    @original_maze.setter
    def original_maze(self, value):
        raise RuntimeError("Do not try and change the original maze.")
    
    @abstractmethod
    def solve(self) -> Tuple[Coords]:
        raise NotImplementedError(f"This method must be implemented")

    def solver_stats(self):
        # TODO -> add a read out of solved information here

        # Turn off visualization and then reapply after solving
        original_vis_setting = self.visualize
        self.visualize = False

        start_time = time.time()
        path = self.solve()
        end_time = time.time()

        self.visualize = original_vis_setting

        stats = {
            "valid_path": self.validate_path(path),
            "path": path,
            "path_length": len(path),
            "solve_time": end_time - start_time,
        }

        return stats

    def validate_path(self, path: Tuple[Coords]):
        # TODO -> add path validation test
        return True
