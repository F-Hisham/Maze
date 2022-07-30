from maze.basic_maze import Maze
from maze.cells import Coords
from solvers.simple import PseudoDirectionalMazeSolver, SimpleMazeSolver


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

    maze_solver = SimpleMazeSolver(maze, start, end, visualize=True)
    solver_stats = maze_solver.solver_stats(n=100)    
    print(solver_stats)
    temp = 1


if __name__ == "__main__":
    main()
