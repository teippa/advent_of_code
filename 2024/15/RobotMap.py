
from math import inf
from typing import Generator
from Coordinate import Coordinate
from enum import IntEnum

class MapObject(IntEnum):
    EMPTY = -1
    WALL = 0
    OBSTACLE = 1
    ROBOT = 10

def coordinate_sum(a: Coordinate, b: Coordinate):
    """ This is implemented in Coordinate with __add__,
    but for some reason I get 
    TypeError: unsupported operand type(s) for +: 'Coordinate' and 'Coordinate'

    And interesting thing is that it works in Coordinate.py, but not in this file
    """
    return Coordinate(a.x+b.x , a.y+b.y)

class MapData:
    data: list[list[int]] = None
    _shape: tuple[int,int] = None
    def __init__(self, mapData):
        self.data = self._load_map(mapData)

    def _load_map(self, mapData: str) -> tuple[tuple[int]]:
        translate_str = {
            '#': MapObject.WALL,
            '.': MapObject.EMPTY,
            'O': MapObject.OBSTACLE,
            '@': MapObject.ROBOT,
        }

        return [
            [ translate_str[x] for x in row ]
            for row in mapData.split('\n')
        ]
    
    def __repr__(self) -> str:
        chars = '#O????????@.'
        return '\n'.join((
            ''.join(chars[i] for i in row)
            for row in self.data
        ))
    
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
    
    def try_get(self, x: int, y: int, default: int|None = None) -> int:
        try:
            return self[x, y]
        except IndexError:
            return default
        
    def try_set(self, x: int, y: int, value) -> bool:
        try:
            self[x, y] = value
            return True
        except IndexError:
            return False
        
    def rows(self) -> Generator[tuple[MapObject, ...], None, None]:
        for row in self.data:
            yield row
    
    def __iter__(self) -> Generator[tuple[Coordinate, MapObject], None, None]:
        for y, row in enumerate(self.data):
            for x, value in enumerate(row):
                yield(Coordinate(x, y), value)
    
    def move_obstacle(self, old_pos, new_pos):
        if self[old_pos] != MapObject.OBSTACLE:
            raise ValueError('No movable obstacle in position', old_pos)
        if self[new_pos] != MapObject.EMPTY:
            raise ValueError("Can't move obstacle to position, because it is occupied", new_pos)
        self[old_pos] = MapObject.EMPTY
        self[new_pos] = MapObject.OBSTACLE


class RobotMap:
    start_position: Coordinate = None
    data: MapData = None
    robot: Coordinate = None
    _directions_str = ''
    _direction_cursor: int = 0
    def __init__(self, mapData, directions):
        self.data = MapData(mapData)
        self._directions_str = directions.replace('\n', '')
        self.start_position = self._find_starting_position()
        self.reset()
        
    def reset(self):
        # Set to default values
        self.robot = Coordinate(*self.start_position)
        self._direction_cursor = 0

    
    def _direction_str2coord(self, s):
        str2Coord = {
            '^': Coordinate.UP(),
            '>': Coordinate.RIGHT(),
            'v': Coordinate.DOWN(),
            '<': Coordinate.LEFT()
        }
        return str2Coord[s]

    def iter_directions(self):
        for i, d in enumerate(self._directions_str):
            self._direction_cursor = i
            yield self._direction_str2coord(d)
    
    def _find_starting_position(self):
        for position, value in self.data:
            if value == MapObject.ROBOT:
                self.data[position] = MapObject.EMPTY
                return position
        raise ValueError("Position not found!")
    
        
    
    
    @property
    def shape(self) -> tuple[int,int]:
        return self.data.shape
    
    def __repr__(self) -> str:
        s = self.data.__repr__()
        # rows = s.split('\n')
        # rows[self.robot.y][self.robot.x] = 
        # return '\n'.join(rows)
        print(self.robot)
        r = self._directions_str[self._direction_cursor]
        index = (self.robot.y * (self.shape[1]+1)) + self.robot.x

        return s[:index] + r + s[index+1:]
    
    def try_move_obstacle(self, obstacle_pos: Coordinate, obstacle_dir: Coordinate) -> bool:
        next_pos = coordinate_sum(obstacle_pos, obstacle_dir)
        
        if self.data[next_pos] == MapObject.OBSTACLE:
            self.try_move_obstacle(next_pos, obstacle_dir)

        if self.data[next_pos] == MapObject.EMPTY:
            self.data.move_obstacle(obstacle_pos, next_pos)
            return True
        return False

        
    def try_move_robot(self, direction: Coordinate):
        next_pos = coordinate_sum(self.robot, direction)
        if self.data[next_pos] == MapObject.OBSTACLE:
            self.try_move_obstacle(next_pos, direction)

        if self.data[next_pos] == MapObject.EMPTY:
            self.robot = next_pos
            return True
        return False

    def move_boxes(self, max_iter=inf):
        for i, direction in enumerate(self.iter_directions()):
            if i>max_iter : 
                return
            # print(self.robot, direction)

            self.try_move_robot(direction)
            # print(self)

    
    def obstacle_GPS(self):
        for position, value in self.data:
            if value == MapObject.OBSTACLE:
                yield 100*position.y + position.x



    