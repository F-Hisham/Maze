from dataclasses import dataclass
from typing import Optional, Tuple

from maze.constants import Locations


@dataclass
class Coords:
    x: int
    y: int

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


@dataclass
class CellValue:
    cell_type: Locations


class CellArray:
    # TODO -> decouple CellType from the set and get etc.
    def __init__(self, nested_cells: Tuple[Tuple[CellValue]]) -> None:
        self.array = nested_cells
    
    def get_cell_type(self, coords: Coords) -> Locations:
        cell_type = self.array[coords.y][coords.x].cell_type
        return cell_type
    
    def set_cell_type(self, coords: Coords, cell_type: Locations):
        self.array[coords.y][coords.x].cell_type = cell_type
    
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
        return 0 <= coords.y < self.num_rows and 0 <= coords.x < self.num_cols
           
    def up(self, coords: Coords) -> Optional[Coords]:
        up = Coords(coords.x - 1, coords.y)
        return up if self.is_in_bounds(up) else None
    
    def down(self, coords: Coords) -> Optional[Coords]:
        down = Coords(coords.x + 1, coords.y)
        return down if self.is_in_bounds(down) else None
    
    def left(self, coords: Coords) -> Optional[Coords]:
        left = Coords(coords.x , coords.y - 1)
        return left if self.is_in_bounds(left) else None
    
    def right(self, coords: Coords) -> Optional[Coords]:
        right = Coords(coords.x , coords.y + 1)
        return right if self.is_in_bounds(right) else None
    
    def adjacent_cells(self, coords: Coords) -> Tuple[Optional[Coords]]:
        cells = (
            self.up(coords), 
            self.down(coords), 
            self.left(coords), 
            self.right(coords)
        )
        return tuple(cell for cell in cells if cell)
    
    def is_adjacent(self, coords: Coords, other_coords: Coords) -> bool:
        return other_coords in self.adjacent_cells(coords)
    
    @classmethod
    def load_from_iterables(cls, iterables):
        row_lengths = [len(row) for row in iterables]
        max_row_len = max([len(row) for row in iterables])
        if not all([row_len == max_row_len for row_len in row_lengths]):
            raise RuntimeError(
                f"Expected equal length rows, instead got lengths of: {row_lengths}"
            )
        
        nested_tuples = tuple(
            tuple(CellValue(Locations(val)) for val in row) for row in iterables
        )
        
        return CellArray(nested_tuples)
    
    def __repr__(self) -> str:
        string_list = []
        for row in self.array:
            string_list.append("\n")
            string_list.extend([str(cell.cell_type.value) for cell in row])
        return " ".join(string_list)        
    

def main():
    maze = CellArray.load_from_iterables(iterables=[
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
    temp = 1
    
    
if __name__=="__main__":
    main()
