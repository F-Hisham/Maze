from maze.basic_maze import Maze
from maze.cells import Coords
from solvers.simple import PseudoDirectionalMazeSolver


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

    maze_solver = PseudoDirectionalMazeSolver(maze, start, end, visualize=True)
    solver_stats = maze_solver.solve()    
    print(solver_stats)
    temp = 1


if __name__ == "__main__":
    main()
