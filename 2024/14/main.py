# https://adventofcode.com/2024/day/14
#%% ----------- SETUP -------------------------
from math import prod
import os
from sys import path as SYSPATH

script_path = os.path.dirname(os.path.abspath(__file__))

SYSPATH.append(os.path.join(script_path, '../..'))
from utils import load_data, execute_function

#% --------- THE IMPORTANT STUFF -------------

# FILENAME = 'example_input.txt'
FILENAME = 'input.txt'
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

def keep_in_room(pos, room):
    return Coordinate(
        (pos.x % room.x),
        (pos.y % room.y)
    )

def future_position(pos: Coordinate, vel: Coordinate, room, time_skip_s: int = 1) -> Coordinate:
    new_pos = Coordinate(
        pos.x + vel.x*time_skip_s,
        pos.y + vel.y*time_skip_s,
    )
    return keep_in_room(new_pos, room)



def room_middle_coordinates(room: Coordinate):
    return Coordinate(
        room.x//2,
        room.y//2,
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

def task_1():
    data = load_data(file_path, lines=True, dtype=parse_row)

    room_size = Coordinate(101, 103)
    robots = []
    for p0, v in data:
        p1 = future_position(p0, v, room_size, time_skip_s=100)
        robots.append(p1)
    quads = count_quadrants(robots, room_size)

    return prod(quads)




def is_many_positions_in_line(positions):
    consecutives = 0
    prev_x = 0
    for p in sorted(positions, key=lambda p: (p.y, p.x)):
        if (prev_x+1 == p.x):
            consecutives += 1
        prev_x = p.x
    if consecutives/len(positions) > .3:
        # print(consecutives/len(positions))
        return True
    return False

def task_2():
    data = load_data(file_path, lines=True, dtype=parse_row)
    
    room_size = Coordinate(101, 103)
    positions, velocities = zip(*data)
    
    for seconds in range(1, 10_000):
        positions = [
            future_position(p0, v, room_size)
            for p0, v in zip(positions, velocities)
        ]
        if is_many_positions_in_line(positions):
            # If something like 30% of points are in line, 
            # there may be some structure there
            return seconds




#% -------------------------------------------

if __name__ == "__main__":
    do_timing = False

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

# Function: task_1()
# 	Result: 230900224
# 	Execution time: 8.9982 ms.
# Function: task_2()
# 	Result: 6532
# 	Execution time: 10.3336 s.