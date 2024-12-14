# https://adventofcode.com/2024/day/14
#%% ----------- SETUP -------------------------
from math import prod
import os
from sys import path as SYSPATH

script_path = os.path.dirname(os.path.abspath(__file__))

SYSPATH.append(os.path.join(script_path, '..'))
from utils import load_data, execute_function

#% --------- THE IMPORTANT STUFF -------------

FILENAME = 'example_input.txt'
# FILENAME = 'input.txt'
file_path = os.path.join(script_path, FILENAME)

import re

from typing import Iterable, NamedTuple

class Coordinate(NamedTuple):
    x: int
    y: int


def parse_row(s: str) -> tuple[Coordinate, Coordinate]:
    match = re.match(r'p=(?P<pos>-?\d+,-?\d+) v=(?P<vel>-?\d+,-?\d+)', s)
    pos = Coordinate(*map(int, match.group('pos').split(',')))
    vel = Coordinate(*map(int, match.group('vel').split(',')))
    return pos, vel

def future_position(p0: Coordinate, vel: Coordinate, time_skip_s: int = 1) -> Coordinate:
    return Coordinate(
        p0.x + vel.x*time_skip_s,
        p0.y + vel.y*time_skip_s,
    )

def keep_in_room(p0, room):
    return Coordinate(
        (p0.x % room.x) + (p0.x<0),
        (p0.y % room.y) + (p0.y<0),
    )

def room_middle_coordinates(room: Coordinate):
    return Coordinate(
        room.x//2+1,
        room.y//2+1,
    )

def count_quadrants(robots: Iterable[Coordinate], room: Coordinate):
    pit = room_middle_coordinates(room)
    quads = [0,0,0,0]
    for robot in robots:
        if robot.x < pit.x and robot.y < pit.y:
            quads[0] += 1
        if robot.x < pit.x and robot.y > pit.y:
            quads[1] += 1
        if robot.x > pit.x and robot.y < pit.y:
            quads[2] += 1
        if robot.x > pit.x and robot.y > pit.y:
            quads[3] += 1
    return quads

def test():
    room_size = Coordinate(7, 11)
    data = load_data(file_path, lines=True, dtype=parse_row)
    robots = []
    for p0, v in data:
        p1 = future_position(p0, v, time_skip_s=100)
        p1 = keep_in_room(p1, room_size)
        robots.append(p1)
    quads = count_quadrants(robots, room_size)
    
    import numpy as np
    
    asd = np.zeros(room_size)
    print(asd, asd.shape)
    print(robots)
    for p in robots:
        asd[p.y, p.x] += 1
    
    print(prod(quads))


def task_1():
    room_size = Coordinate(101, 103)
    # print(quads)
    # print(room_size)
    return 

def task_2():
    # data = load_data(file_path)
    return



#% -------------------------------------------

if __name__ == "__main__":
    do_timing = False

    test()

    execute_function(
        task_1,
        args = {},
        do_timing = do_timing
    )
    
    execute_function(
        task_2,
        args = {},
        do_timing = do_timing
    )
    