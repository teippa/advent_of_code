from __future__ import annotations

from collections import defaultdict, deque
from math import inf
from typing import Generator, Iterable
from enum import IntEnum
from typing import NamedTuple
from numbers import Number

class MapObject(IntEnum):
    EMPTY = 0
    OBSTACLE = 1
    VISITED = 2


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


class MapData:
    _str_mapping = '·█●○' # Indexes correspond to MapObject values
    data: list[list[IntEnum]] = None
    _shape: tuple[int,int] = None
    def __init__(self, map_size: str):
        self.data = self._initialize_map(map_size)

    def _initialize_map(self, map_size: int) -> tuple[tuple[int]]:
        return [
            [0,] * map_size
            for _ in range(map_size)
        ]
        
    def _draw_box_around(self, s: str):
        h_line = '─'*len(self.data)
        lines = (
            f"┌{h_line}┐",
            *(
                '│' + row + '│'    
                for row in s.split('\n')
            ),
            f"└{h_line}┘"
        )
        return '\n'.join(lines)
    
    def __repr__(self) -> str:
        s = '\n'.join(
            ''.join(self._str_mapping[i] for i in row)
            for row in self.data
        )
        return self._draw_box_around(s)
        # return s

    
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
    


class MemoryMap:
    position_end: Coordinate = None
    position_start: Coordinate = None
    data: MapData = None
    def __init__(self, map_size: int):
        self.data = MapData(map_size)
        self.position_start = Coordinate(0,0)
        self.position_end = Coordinate(map_size-1, map_size-1)
        self.reset()
    
    def reset(self):
        # Set to default values
        pass

    # def _find_position(self, object: MapObject, replace_with_empty: bool = True) -> Coordinate:
    #     for position, value in self.data:
    #         if value == object:
    #             if replace_with_empty:
    #                 print(f"Position: {position}. Replacing {object} with {MapObject.EMPTY}")
    #                 self.data[position] = MapObject.EMPTY
    #             return position
    #     raise ValueError("Position not found!")
    
    @property
    def shape(self) -> tuple[int,int]:
        return self.data.shape

    def __repr__(self) -> str:
        return repr(self.data)
    
    def set_corrupted(self, position: Coordinate):
        self.data[position] = MapObject.OBSTACLE
    
    def set_corrupted_many(self, positions: Iterable[Coordinate]):
        for pos in positions:
            self.set_corrupted(pos)
            
    def not_wall(self, obj):
        return obj is not None and obj != MapObject.OBSTACLE
    
    def get_path_next_positions(self, position: Coordinate):
        for direction in Coordinate.CARDINALS():
            next_position = position + direction
            object_in_direction = self.data.try_get(next_position)
            if self.not_wall(object_in_direction):
                yield next_position
    
    
    def find_path_distance(self, early_stop = False):
        """ Count distance to the end from each position
            on the path
        """
        
        distances = defaultdict(lambda: [None,None]) # distances from positions to start and end positions
        forward_position_queue = deque((
            (self.position_start, 0),
        ))
        backward_position_queue = deque((
            (self.position_end, 0),
        ))
        i = 0
        while forward_position_queue and backward_position_queue:
            i += 1
            if early_stop and i>20_000:
                # After this, we have reached the gap thing
                return None
            # FWD
            position, distance = forward_position_queue.popleft()
            self.data[position] = MapObject.VISITED
            distances[position][0] = distance
            # if position == self.position_end:
            #     return distance

            for next_pos in self.get_path_next_positions(position):
                if distances[next_pos][1] is not None:
                    return distances[next_pos][1] + distance +1
                if distances[next_pos][0] is None:
                    forward_position_queue.append((
                        next_pos, distance+1
                    ))
                
            # BWD
            position, distance = backward_position_queue.popleft()
            self.data[position] = MapObject.VISITED
            distances[position][1] = distance
            # if position == self.position_start:
            #     return distance

            for next_pos in self.get_path_next_positions(position):
                if distances[next_pos][0] is not None:
                    return distances[next_pos][0] + distance +1
                if distances[next_pos][1] is None:
                    backward_position_queue.append((
                        next_pos, distance+1
                    ))
            
        
        return -1
