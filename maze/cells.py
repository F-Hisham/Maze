from dataclasses import dataclass
from enum import Enum
from typing import Optional, Tuple

from typing_extensions import Self


class CellValues(Enum):

    ROAD = 0
    BLOCK = 1
    PATH = 2


@dataclass
class Coords:
    x: int
    y: int

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    #Not allowed to change this class
    # def __sub__(self, other):
    #     return Coords(self.x - other.x, self.y - other.y)

    def apply_move(self, move_coords: Self) -> Self:
        return Coords(self.x + move_coords.x, self.y + move_coords.y)


class Moves:
    __slots__ = []
    UP = Coords(-1, 0)
    DOWN = Coords(1, 0)
    LEFT = Coords(0, -1)
    RIGHT = Coords(0, 1)
    ALL = [UP, DOWN, LEFT, RIGHT]


class Cell:

    __slots__ = ["_value"]

    def __init__(self, value: CellValues):
        self._value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        current_val = self.value
        value = CellValues(val)
        if current_val == CellValues.BLOCK:
            raise RuntimeError(f"Cannot change value of type {CellValues.BLOCK}.")
        else:
            self._value = value


class CellArray:
    
    def __init__(self, nested_cells: Tuple[Tuple[Cell]]) -> None:
        self.array = nested_cells

    def get_cell_value(self, coords: Coords) -> CellValues:
        return self.array[coords.y][coords.x].value

    def set_cell_value(self, coords: Coords, cell_value: CellValues) -> None:
        self.array[coords.y][coords.x].value = cell_value

    @property
    def num_rows(self) -> int:
        return len(self.array)

    @property
    def num_cols(self) -> int:
        row_lengths = [len(x) for x in self.array]
        max_row_len = max(row_lengths)
        if not all([row_len == max_row_len for row_len in row_lengths]):
            raise RuntimeError(
                f"Expected equal length rows, instead got lengths of: {row_lengths}"
            )
        else:
            return max_row_len

    def is_in_bounds(self, coords: Coords) -> bool:
        """Are given coords in the cell array."""
        return 0 <= coords.y < self.num_rows and 0 <= coords.x < self.num_cols

    def in_bounds_move(self, coords: Coords, move: Coords) -> Optional[Coords]:
        """Apply move to coords. If the final coords are inside the array then
        return new coords. If the final coords are outside the array then return
        None."""
        new_coords = coords.apply_move(move)
        return new_coords if self.is_in_bounds(new_coords) else None
                
    def up(self, coords: Coords) -> Optional[Coords]:
        """Return the coords above the given coords if in bounds."""
        return self.in_bounds_move(coords, Moves.UP)

    def down(self, coords: Coords) -> Optional[Coords]:
        """Return the coords below the given coords if in bounds."""
        return self.in_bounds_move(coords, Moves.DOWN)

    def left(self, coords: Coords) -> Optional[Coords]:
        """Return the coords to the left of the given coords if in bounds."""
        return self.in_bounds_move(coords, Moves.LEFT)

    def right(self, coords: Coords) -> Optional[Coords]:
        """Return the coords to the right of the given coords if in bounds."""
        return self.in_bounds_move(coords, Moves.RIGHT)

    def adjacent_cells(self, coords: Coords) -> Tuple[Coords]:
        """Return all in bound cells that are up, down, left or right from the
        given coords."""
        cells = (
            self.up(coords),
            self.down(coords),
            self.left(coords),
            self.right(coords),
        )
        return tuple(cell for cell in cells if cell)

    def is_adjacent(self, coords: Coords, other_coords: Coords) -> bool:
        """Are the two sets of coordinates adjacent (ignoring diagonals)."""
        return other_coords in self.adjacent_cells(coords)

    @property
    def value_array(self):
        """Return an array of just the values in each cell."""
        value_array = tuple(
            (tuple((cell.value.value for cell in row)) for row in self.array)
        )
        return value_array

    @classmethod
    def load_from_iterables(cls, iterables):
        row_lengths = [len(row) for row in iterables]
        max_row_len = max([len(row) for row in iterables])
        if not all([row_len == max_row_len for row_len in row_lengths]):
            raise RuntimeError(
                f"Expected equal length rows, instead got lengths of: {row_lengths}"
            )

        nested_tuples = tuple(
            tuple(Cell(CellValues(val)) for val in row) for row in iterables
        )

        return CellArray(nested_tuples)

    def __repr__(self) -> str:
        string_list = []
        for row in self.value_array:
            string_list.append("\n")
            string_list.extend([str(val) for val in row])
        return " ".join(string_list)


def main():
    maze = CellArray.load_from_iterables(
        iterables=[
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
    temp = 1


if __name__ == "__main__":
    main()
