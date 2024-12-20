from __future__ import annotations

from collections import defaultdict, deque
from math import inf
from typing import Generator, Iterable
from enum import IntEnum
from typing import NamedTuple
from numbers import Number


class Coordinate(NamedTuple):
    x: int
    y: int
    
    def __repr__(self):
        return f"Coord[{self.x},{self.y}]"

    def __add__(self, direction:Coordinate) -> Coordinate:
        if isinstance(direction, Coordinate):
            return Coordinate(self.x + direction.x, self.y + direction.y)
        elif isinstance(direction, Number):
            return Coordinate(self.x + direction, self.y + direction)
        raise NotImplementedError  # raise NotImplementedError if other is not a Point
    
    def __mul__(self, value: Number) -> Coordinate:
        if isinstance(value, Number):
            return Coordinate(value * self.x, value * self.y)
        raise NotImplementedError  # raise NotImplementedError if other is not a Point
    
    def __eq__(self, other: Coordinate):
        if isinstance(other, Coordinate):
            return (other.x == self.x) and (other.y == self.y)
        raise NotImplementedError  # raise NotImplementedError if other is not a Point
    
    @property
    def manhattan_distance(self) -> int:
        """ manhattan distance: |x| + |y|
        """
        return abs(self.x) + abs(self.y)
    
    @classmethod
    def UP(cls) -> Coordinate:
        return cls(0,-1)
        
    @classmethod
    def DOWN(cls) -> Coordinate:
        return cls(0,1)
        
    @classmethod
    def LEFT(cls) -> Coordinate:
        return cls(-1,0)
        
    @classmethod
    def RIGHT(cls) -> Coordinate:
        return cls(1,0)
    
    @classmethod
    def CARDINALS(cls) -> Iterable[Coordinate]:
        return (
            cls.UP(),
            cls.RIGHT(),
            cls.DOWN(),
            cls.LEFT(),
        )

class MapObject(IntEnum):
    EMPTY = -1
    WALL = 0
    FOOTPRINT = 1
    START = 2
    END = 3

class MapData:
    data: list[list[int]] = None
    _shape: tuple[int,int] = None
    print_map: str = '█XSE '
    def __init__(self, mapData: str):
        self.data = self._load_map(mapData)

    def _load_map(self, mapData: str) -> tuple[tuple[int]]:
        translate_str = {
            '#': MapObject.WALL,
            '.': MapObject.EMPTY,
            'S': MapObject.START,
            'E': MapObject.END,
        }

        return [
            [ translate_str[x] for x in row ]
            for row in mapData.split('\n')
        ]
    
    def __repr__(self) -> str:
        return '\n'.join((
            ''.join(self.print_map[i] for i in row)
            for row in self.data
        ))
        
    def is_on_path(self, position: Coordinate) -> bool:
        value = self.try_get(position)
        return value is not None and value != MapObject.WALL
    
    @property
    def shape(self):
        if self._shape is not None:
            return self._shape
        if self.data is not None and len(self.data):
            self._shape = (len(self.data[0]), len(self.data))
        return self._shape

    def __getitem__(self, position: Coordinate) -> MapObject:
        x, y = position
        if x<0 or y<0:
            raise IndexError
        return self.data[y][x]
    
    def __setitem__(self, position: Coordinate, value: int) -> bool:
        x, y = position
        if x<0 or y<0:
            raise IndexError
        self.data[y][x] = value
    
    def try_get(self, position: Coordinate, default: int|None = None) -> int:
        try:
            return self[position]
        except IndexError:
            return default
        
    def try_set(self, position: Coordinate, value) -> bool:
        try:
            self[position] = value
            return True
        except IndexError:
            return False
    
    @property
    def rows(self) -> Generator[tuple[MapObject, ...], None, None]:
        for row in self.data:
            yield row
    
    def __iter__(self) -> Generator[tuple[Coordinate, MapObject], None, None]:
        for y, row in enumerate(self.data):
            for x, value in enumerate(row):
                yield(Coordinate(x, y), value)
    


class RaceMap:
    position_end: Coordinate = None
    position_start: Coordinate = None
    data: MapData = None
    distances = None
    def __init__(self, mapData: str):
        self.data = MapData(mapData)
        self.position_start = self._find_position(
            MapObject.START,
            replace_with_empty=False
        )
        self.position_end = self._find_position(
            MapObject.END,
            replace_with_empty=False
        )
        self.reset()
        
    def reset(self):
        # Set to default values
        self.distances = dict()
        pass

    def _find_position(self, object: MapObject, replace_with_empty: bool = True) -> Coordinate:
        for position, value in self.data:
            if value == object:
                if replace_with_empty:
                    print(f"Position: {position}. Replacing {object} with {MapObject.EMPTY}")
                    self.data[position] = MapObject.EMPTY
                return position
        raise ValueError("Position not found!")
    
    @property
    def shape(self) -> tuple[int,int]:
        return self.data.shape

    def __repr__(self) -> str:
        self_str = ''
        for y, row in enumerate(self.data.rows):
            for x, value in enumerate(row):
                if value == MapObject.WALL:
                    self_str += '█'
                elif value == MapObject.FOOTPRINT:
                    self_str += str(self.distances[Coordinate(x,y)]%10)
                else:
                    self_str += '#OSE '[value]

            self_str += '\n'
        return self_str
    
    def get_path_next_positions(self, position: Coordinate):
        for direction in Coordinate.CARDINALS():
            next_position = position + direction
            object_in_direction = self.data[next_position]
            if object_in_direction in {MapObject.EMPTY, MapObject.START, MapObject.END}:
                yield next_position
                    
    def calculate_paths(self):
        """ Count distance to the end from each position
            on the path
        """
        next_position_queue = deque((
            (self.position_end, 0),
        ))
        
        while next_position_queue:
            position, distance = next_position_queue.popleft()
            self.distances[position] = distance
            self.data[position] = MapObject.FOOTPRINT

            
            for next_pos in self.get_path_next_positions(position):
                next_position_queue.append((
                    next_pos, distance+1
                ))
            
        
        
