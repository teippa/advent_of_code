
from typing import Iterable

"""
    This thing takes positions and creates an area from them
    Then the area is scanned horizontally and vertically
    Scanning counts continuous edges along rows (and columns)
      and thats pretty much it
"""

class RegionScanner:
    region = None
    _region_T = None
    shape = None
    
    def __init__(self, region_positions):
        self.region = self.get_region_shape(region_positions)
        

    def get_region_shape(self, positions: Iterable[tuple[int,int]]):
        positions = tuple(positions)
        
        shift_x = min(positions, key=lambda p: p[0])[0] - 1 # -1 to add extra col for scanner
        shift_y = min(positions, key=lambda p: p[1])[1] - 1 # -1 to add extra row for scanner
        size_x = max(positions, key=lambda p: p[0])[0] - shift_x + 2
        size_y = max(positions, key=lambda p: p[1])[1] - shift_y + 2
        self.shape = (size_x, size_y)
        region = [
            [
                int((x+shift_x, y+shift_y) in positions)
                for x in range(size_x)
            ]
            for y in range(size_y)
        ]
        return region

    def __repr__(self):
        return '\n'.join(
            ''.join(
                '#' if inside else '.' 
                for inside in row
            )
            for row in self.region
        )
    
    @property
    def area(self):
        return sum(
            sum(row)
            for row in self.region
        )
    
    @property
    def region_T(self):
        if self._region_T is None:
            self._region_T = [[] for _ in range(self.shape[0])]
            for row in self.region:
                for i, x in enumerate(row):
                    self._region_T[i].append(x)
        return self._region_T
    
    def get_column(self, index: int):
        if index < 0: raise IndexError("Negative indexes aren't allowed")
        return tuple(self.region_T[index])
    
    def get_row(self, index: int):
        if index < 0: raise IndexError("Negative indexes aren't allowed")
        return tuple(self.region[index])
    
    def scan(self, region):
        n_fence = 0
        for i, row in enumerate(region[:-1]):
            previous_state = None
            for j, is_pot in enumerate(row):
                is_pot_down_east = region[i+1][j]
                state = (is_pot, is_pot_down_east)
                if (is_pot_down_east != is_pot) and (state != previous_state):
                    n_fence += 1
                previous_state = state
        return n_fence
    
    def scan_rows(self):
        return self.scan(self.region)
    
    def scan_columns(self):
        return self.scan(self.region_T)
    
    def scan_region(self):
        return self.scan_rows() + self.scan_columns()