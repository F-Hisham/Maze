from dataclasses import dataclass


@dataclass
class Coords:
    x: int
    y: int

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


@dataclass
class Cell:
    x: int
    y: int
    max_x: int
    max_y: int

    def coords_equal(self, other):
        return self.x == other.x and self.y == other.y
    
    def limits_equal(self, other):
        return self.max_x == other.max_x and self.max_y == other.max_y
        
    def __eq__(self, other):
        return self.coords_equal(other) and self.limits_equal(other)

    def is_in_bounds(self, x, y):
        return 0 <= x < self.max_x and 0 <= y < self.max_y
    
    def new_cell(self, x, y):
        if self.is_in_bounds(x, y):
            return Cell(x, y, max_x=self.max_x, max_y=self.max_y)
        else:
            return None
        
    @property
    def up(self):
        new_x, new_y = self.x, self.y
        return self.new_cell(x=new_x, y=new_y)
    
    @property
    def down(self):
        new_x, new_y = self.x + 1, self.y
        return self.new_cell(x=new_x, y=new_y)
    
    @property
    def left(self):
        new_x, new_y = self.x, self.y - 1
        return self.new_cell(x=new_x, y=new_y)
    
    @property
    def right(self):
        new_x, new_y = self.x, self.y + 1
        return self.new_cell(x=new_x, y=new_y)
    
    @property
    def adjacent_cells(self):
        return [self.up, self.down, self.left, self.right]
    
    def is_adjacent(self, other_cell):
        return other_cell in self.adjacent_cells
            

def main():
    cell_a = Cell(1, 1, 10, 10)
    cell_b = Cell(1, 2, 10 , 10)
    temp = 1
