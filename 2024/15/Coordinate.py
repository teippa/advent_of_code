#%%
from __future__ import annotations

from typing import NamedTuple, SupportsIndex
from numbers import Number

class Coordinate(NamedTuple):
    x: int
    y: int

    def __add__(self, direction:Coordinate) -> Coordinate:
        if isinstance(direction, Coordinate):
            return Coordinate(self.x + direction.x, self.y + direction.y)
        elif isinstance(direction, Number):
            return Coordinate(self.x + direction, self.y + direction)
        return NotImplemented  # Return NotImplemented if other is not a Point
    
    def __mul__(self, value: Number) -> Coordinate:
        if isinstance(value, Number):
            return Coordinate(value * self.x, value * self.y)
        return NotImplemented  # Return NotImplemented if other is not a Point
    
    def __eq__(self, other: Coordinate):
        if isinstance(other, Coordinate):
            return (other.x == self.x) and (other.y == self.y)
        return NotImplemented  # Return NotImplemented if other is not a Point
    
    @classmethod
    def UP(cls):
        return cls(0,-1)
        
    @classmethod
    def DOWN(cls):
        return cls(0,1)
        
    @classmethod
    def LEFT(cls):
        return cls(-1,0)
        
    @classmethod
    def RIGHT(cls):
        return cls(1,0)
    
if __name__ == '__main__':
    print(Coordinate(1,7) + Coordinate.UP())

