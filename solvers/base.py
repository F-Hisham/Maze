import random
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional, Tuple

from maze.basic_maze import Maze
from maze.cells import Coords


@dataclass
class SolverResult:
    path: Tuple[Coords]
    is_valid_path: bool
    path_length: int
    solve_time: float


@dataclass
class SolverStats:
    solver_class: str
    results_sets: List[SolverResult]

    @property
    def valid_path_results(self) -> Tuple[bool]:
        return tuple((res.is_valid_path for res in self.results_sets))

    @property
    def path_lengths(self) -> Tuple[int]:
        return tuple((res.path_length for res in self.results_sets))

    @property
    def solve_times(self) -> Tuple[float]:
        return tuple((res.solve_time for res in self.results_sets))

    @property
    def all_paths_valid(self):
        return all(self.valid_path_results)

    @property
    def length_stats(self):
        return {
            "mean": sum(self.path_lengths) / len(self.path_lengths),
            "min": min(self.path_lengths),
            "max": max(self.path_lengths),
        }

    @property
    def length_score(self):
        return self.length_stats.values()

    @property
    def solve_time_stats(self):
        return {
            "mean": sum(self.solve_times) / len(self.solve_times),
            "min": min(self.solve_times),
            "max": max(self.solve_times),
        }

    @property
    def timer_score(self):
        return sum(self.solve_time_stats.values()) * 50

    @property
    def total_score(self):
        if self.all_paths_valid:
            return self.length_score + self.timer_score
        else:
            return None

    def __repr__(self) -> str:
        return (
            f"Solver stats for class {self.solver_class}: \n"
            f"Total score for {len(self.results_sets)} tests: {self.total_score:.2f} \n"
            f"All paths valid results: {self.all_paths_valid}\n"
            f"Path length score ({self.length_score:.2f}): {self.length_stats}\n"
            f"Solver timing score ({self.timer_score:.2f}): {self.solve_time_stats}"
        )


class BaseMazeSolver(ABC):
    def __init__(
        self,
        maze: Maze,
        start_coords: Optional[Coords] = None,
        end_coords: Optional[Coords] = None,
        visualize: bool = False,
    ):
        # Do not attempt to modify original maze, it is needed for validation
        self.__original_maze = maze

        # Do not modify the start and end coordinates either
        self.start_coords = start_coords or Coords(0, 0)
        bottom_right = Coords(
            self.original_maze.num_cols - 1, self.original_maze.num_rows - 1
        )
        self.end_coords = end_coords or bottom_right

        # If you have any plotting, make sure it can be turned on and off using
        # the visualize attribute below
        self.visualize = visualize

        # If you have any random number generators, use this for the
        # seed to allow for testing with different random number series
        self.rand_seed = 1

        self.validate_start_coords()
        self.validate_end_coords()

    @property
    def original_maze(self):
        return self.__original_maze

    @original_maze.setter
    def original_maze(self, value):
        raise RuntimeError("Do not try and change the original maze.")

    def validate_start_coords(self):
        if not self.original_maze.is_valid_road(self.start_coords):
            raise RuntimeError(
                f"Start coords {self.start_coords} is not a valid road "
                f"in maze {self.original_maze}."
            )

    def validate_end_coords(self):
        if not self.original_maze.is_valid_road(self.end_coords):
            raise RuntimeError(
                f"End coords {self.end_coords} is not a valid road "
                f"in maze {self.original_maze}."
            )

    @abstractmethod
    def solve(self) -> Tuple[Coords]:
        raise NotImplementedError(f"This method must be implemented")

    def profile_solve(self) -> SolverResult:
        """Profile the solve method for a single run."""
        # Turn off visualization and then reapply after solving
        original_vis_setting = self.visualize
        self.visualize = False

        start_time = time.time()
        path = self.solve()
        end_time = time.time()
        run_time = end_time - start_time

        self.visualize = original_vis_setting

        solver_result = SolverResult(
            path=path,
            is_valid_path=self.validate_path(path),
            path_length=len(path),
            solve_time=run_time,
        )
        return solver_result

    def solver_stats(self, n=100):
        seeds = [random.randint(1, 1_000_000) for i in range(n)]

        results_list = []

        for seed in seeds:
            random.seed(1)
            solver_results = self.profile_solve()
            results_list.append(solver_results)

        solver_stats = SolverStats(
            solver_class=self.__class__.__name__, results_sets=results_list
        )
        return solver_stats

    def validate_path(self, path: Tuple[Coords]):
        is_start = path[0] == self.start_coords
        is_end = path[-1] == self.end_coords

        path_pairs = tuple(zip(path[:-1], path[1:]))
        is_all_adjacent = all(
            [self.original_maze.cell_array.is_adjacent(a, b) for a, b in path_pairs]
        )
        is_all_road = all([self.original_maze.is_valid_road(x) for x in path])

        return all([is_start, is_end, is_all_adjacent, is_all_road])

