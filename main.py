from maze.maze_objs import Maze
from maze.cells import Coords
from solvers.original import MazeSolver


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
