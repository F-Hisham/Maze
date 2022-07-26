from maze.constants import Locations
from maze.cells import Coords, CellArray
from matplotlib import pyplot as plt

plt.ion()
MAZE_PLOT, MAZE_AXIS = plt.subplots()


class Maze:

    def __init__(
        self, 
        array, 
        road_symbol: Locations=Locations.ROAD, 
        block_symbol: Locations=Locations.BLOCK
    ):
        self.cell_array = self.sanitize_maze(array, road_symbol, block_symbol)

    @staticmethod
    def sanitize_maze(
        maze, 
        road_symbol: Locations=Locations.ROAD, 
        block_symbol: Locations=Locations.BLOCK
    ) -> CellArray:

        def sanitized_symbol(symbol_in):
            if Locations(symbol_in) == road_symbol:
                return Locations.ROAD.value
            elif Locations(symbol_in) == block_symbol:
                return Locations.BLOCK.value
            else:
                raise RuntimeError(f"Cannot parse symbol {symbol_in}")

        sanitized_maze = [[sanitized_symbol(x) for x in row] for row in maze]
        return CellArray.load_from_iterables(sanitized_maze)

    @property
    def num_rows(self):
        return self.cell_array.num_rows

    @property
    def num_cols(self):
        return self.cell_array.num_cols
    
    def __repr__(self):
        header_indices = list(range(0, self.num_cols))
        header = f"Idx |{header_indices}"
        separation = "_" * len(header)
        formatted_rows = []

        for i, row in enumerate(self.cell_array):
            formatted_rows.append(f" {i}  |{row}")

        output = "\n".join([header, separation, *formatted_rows])
        return output + "\n"

    def value(self, coords: Coords) -> Locations:
        return Locations(self.cell_array.get_cell_type(coords))

    def set_value(self, coords: Coords, val: Locations):
        self.cell_array.set_cell_type(coords, Locations(val))

    def is_valid_road(self, coords: Coords) -> bool:
        if self.cell_array.is_in_bounds(coords):
            return self.cell_array.get_cell_type(coords) == Locations.ROAD
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
        