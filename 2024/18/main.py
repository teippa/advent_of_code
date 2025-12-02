# https://adventofcode.com/2024/day/18
#%% ----------- SETUP -------------------------
import importlib
import os
from sys import path as SYSPATH

from tqdm import tqdm

script_path = os.path.dirname(os.path.abspath(__file__))

SYSPATH.append(os.path.join(script_path, '../..'))
from utils import load_data, execute_function

#% --------- THE IMPORTANT STUFF -------------

FILENAME = 'example_input.txt'
FILENAME = 'input.txt'
file_path = os.path.join(script_path, FILENAME)

import memory_map
try:
    # Reload the modules to reflect changes
    importlib.reload(memory_map)
except ImportError as e:
    print(e)


def task_1():
    data = load_data(
        file_path, 
        lines=True, 
        dtype=lambda line: tuple(map(int, line.split(',')))
    )
    corrupted = tuple(
        memory_map.Coordinate(x,y) 
        for x,y in data
    ) 
    mm = memory_map.MemoryMap(map_size=71)
    mm.set_corrupted_many(corrupted[:1024])
    distance = mm.find_path_distance()
    print(mm)
    
    return distance

def task_2():
    data = load_data(
        file_path, 
        lines=True, 
        dtype=lambda line: tuple(map(int, line.split(',')))
    )
    corrupted = tuple(
        memory_map.Coordinate(x,y) 
        for x,y in data
    ) 
    mm = memory_map.MemoryMap(map_size=71)
    initial_corrupts = 2024 # Lets skip forward in corruption for convenience
    mm.set_corrupted_many(corrupted[:initial_corrupts])
    for corrupt_index in tqdm(range(initial_corrupts, len(corrupted))):
        mm.set_corrupted(corrupted[corrupt_index])
        # print(mm)
        distance = mm.find_path_distance(early_stop=True)
        if distance == -1:
            break
    
    return ','.join(map(str, corrupted[corrupt_index]))



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
# 	Result: 292
# 	Execution time: 1088.2505 s.
# Function: task_2()
# 	Result: 58,44
# 	Execution time: 89.7834 s.