from maze.basic_maze import Maze
from maze.cells import Coords
from solvers.simple import PseudoDirectionalMazeSolver, SimpleMazeSolver


def main():
    maze = Maze.create_maze_from_excel("mazes.xlsx", "maze_a")

    maze_solver_a = SimpleMazeSolver(maze, visualize=True)
    solution = maze_solver_a.solve()
    solver_stats_a = maze_solver_a.solver_stats(n=10)
    print(solver_stats_a)

    temp = 1

#Quick test to check if the project is plugged to Git
if __name__ == "__main__":
    main()
