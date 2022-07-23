from maze.constants import Locations
from maze.cells import Coords
from matplotlib import pyplot as plt

plt.ion()
MAZE_PLOT, MAZE_AXIS = plt.subplots()


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
        