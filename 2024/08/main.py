# https://adventofcode.com/2024/day/8
#%% ----------- SETUP -------------------------
from collections import defaultdict
import os
from sys import path as SYSPATH

script_path = os.path.dirname(os.path.abspath(__file__))

SYSPATH.append(os.path.join(script_path, '../..'))
from utils import load_data, execute_function

#% --------- THE IMPORTANT STUFF -------------

FILENAME = 'example_input.txt'
FILENAME = 'input.txt'
file_path = os.path.join(script_path, FILENAME)

def loop_over_matrix(data):
    for y, row in enumerate(data):
        for x, value in enumerate(row):
            yield x, y, value

def get_tower_locations(tower_map) -> dict[str, list[tuple[int,int]]]:
    empty_space = '.'
    tower_locations = defaultdict(list)
    for x, y, value in loop_over_matrix(tower_map):
        if value == empty_space:
            continue
        tower_locations[value].append((x,y))
    return dict(tower_locations)

def location_inside_map(x: int, y: int, map_size: tuple[int,int]) -> bool:
    return (0 <= x < map_size[0]) and (0 <= y < map_size[1])

def tower_pairs(towers: tuple[tuple[int,int]]):
    for i, t1 in enumerate(towers): 
        for t2 in towers[i+1:]:
            yield (t1, t2)

def get_antinode_locations(p0: tuple, p: tuple, map_size: tuple, repeat=False):
    x0, y0 = p0
    x, y, = p
    dx = x - x0
    dy = y - y0
    
    node_left = lambda i: (x0-(i*dx) , y0-(i*dy))
    node_right = lambda i: (x+(i*dx) , y+(i*dy))
    
    i = 1 # Creating antinodes to one direction
    while True:
        antinode = node_left(i)
        if not location_inside_map(*antinode, map_size):
            break
        yield antinode
        if not repeat:
            break
        i+=1
        
    i = 1  # Creating antinodes to other direction
    while True:
        antinode = node_right(i)
        if not location_inside_map(*antinode, map_size):
            break
        yield antinode
        if not repeat:
            break
        i+=1
            

def task_1():
    tower_map = load_data(file_path, matrix=True)
    tower_map_size = (len(tower_map[0]), len(tower_map))
    
    # lists of tower locations for each tower type
    tower_locations = get_tower_locations(tower_map)
    
    antinodes = set()
    for tower_x_locations in tower_locations.values():
        for loc_1, loc_2 in tower_pairs(tower_x_locations):
            for antinode in get_antinode_locations(loc_1, loc_2, tower_map_size):
                antinodes.add(antinode)
    
    return len(antinodes)

def task_2():
    # Pretty much the same as task 1
    tower_map = load_data(file_path, matrix=True)
    tower_map_size = (len(tower_map[0]), len(tower_map))
    tower_locations = get_tower_locations(tower_map)
    
    antinodes = set()
    for tower_x_locations in tower_locations.values():
        for loc_1, loc_2 in tower_pairs(tower_x_locations):
            for antinode in get_antinode_locations(loc_1, loc_2, tower_map_size, repeat=True):
                antinodes.add(loc_1) # Tower pairs are also antinodes now
                antinodes.add(loc_2) # Tower pairs are also antinodes now
                antinodes.add(antinode)
    
    return len(antinodes)



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
    
# Function: task_1
# 	Result: 269
# 	Execution time: 5.7085 ms.
# Function: task_2
# 	Result: 949
# 	Execution time: 11.6072 ms.
