from calendar import c
from typing import Optional, Tuple

from matplotlib import pyplot as plt
from numpy import iterable

from maze.cells import CellArray, CellValues, Coords
from maze.loaders import ExcelToIterablesMixin

plt.ion()
MAZE_PLOT, MAZE_AXIS = plt.subplots()


class Maze(ExcelToIterablesMixin):
    DEFAULT_ROAD_SYMBOL = CellValues.ROAD
    DEFAULT_BLOCK_SYMBOL = CellValues.BLOCK

    def __init__(
        self,
        array,
        road_symbol: Optional[CellValues] = None,
        block_symbol: Optional[CellValues] = None,
    ):
        road_symbol = road_symbol or self.DEFAULT_ROAD_SYMBOL
        block_symbol = block_symbol or self.DEFAULT_BLOCK_SYMBOL

        self.cell_array = self.sanitize_maze(array, road_symbol, block_symbol)

    @classmethod
    def sanitize_maze(
        cls,
        maze,
        road_symbol: Optional[CellValues] = None,
        block_symbol: Optional[CellValues] = None,
    ) -> CellArray:
        road_symbol = road_symbol or cls.DEFAULT_ROAD_SYMBOL
        block_symbol = block_symbol or cls.DEFAULT_BLOCK_SYMBOL

        def sanitize_symbol(symbol_in):
            if CellValues(symbol_in) == road_symbol:
                return CellValues.ROAD.value
            elif CellValues(symbol_in) == block_symbol:
                return CellValues.BLOCK.value
            else:
                raise RuntimeError(f"Cannot parse symbol {symbol_in}")

        sanitized_maze = [[sanitize_symbol(x) for x in row] for row in maze]
        return CellArray.load_from_iterables(sanitized_maze)

    @property
    def num_rows(self):
        return self.cell_array.num_rows

    @property
    def num_cols(self):
        return self.cell_array.num_cols

    def value(self, coords: Coords) -> CellValues:
        return CellValues(self.cell_array.get_cell_value(coords))

    def set_value(self, coords: Coords, val: CellValues):
        self.cell_array.set_cell_value(coords, CellValues(val))

    def is_valid_road(self, coords: Coords) -> bool:
        if self.cell_array.is_in_bounds(coords):
            return self.cell_array.get_cell_value(coords) == CellValues.ROAD
        else:
            return False

    def adjacent_roads(self, coords: Coords) -> Tuple[Coords]:
        roads = (
            x for x in self.cell_array.adjacent_cells(coords=coords) if self.is_valid_road(x)
        )
        return tuple(roads)

    def apply_path(self, path: Tuple[Coords]):
        for coords in path:
            if self.is_valid_road(coords):
                self.set_value(coords, val=CellValues.PATH)
            else:
                raise RuntimeError(f"Coords {coords} are not a valid road.")

    def plot(self):
        MAZE_AXIS.clear()
        im = MAZE_AXIS.imshow(self.cell_array.value_array)
        plt.pause(interval=0.005)  # type: ignore

    def __repr__(self):
        header_indices = tuple(range(0, self.num_cols))
        header = f"Idx |{header_indices}"
        separation = "_" * len(header)
        formatted_rows = []

        for i, row in enumerate(self.cell_array.value_array):
            formatted_rows.append(f" {i}  |{row}")

        output = "\n".join([header, separation, *formatted_rows])
        return output + "\n"

    @classmethod
    def create_maze_from_excel(
        cls,
        file_path: str,
        sheet_name: Optional[str] = None,
        road_symbol: Optional[CellValues] = None,
        block_symbol: Optional[CellValues] = None,
    ):
        iterable_maze = cls.load_from_excel(file_path, sheet_name)
        return cls(iterable_maze, road_symbol=road_symbol, block_symbol=block_symbol)


def main():
    maze = Maze(
        array=[
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
        ]
    )
    excel_maze = Maze.create_maze_from_excel(
        file_path="C:/Users/Alexander Mottram/OneDrive/Code/MazeSolver/mazes.xlsx"
    )
    temp = 1


if __name__ == "__main__":
    main()
