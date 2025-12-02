# https://adventofcode.com/2024/day/25
#%% ----------- SETUP -------------------------
import os
from sys import path as SYSPATH

script_path = os.path.dirname(os.path.abspath(__file__))

SYSPATH.append(os.path.join(script_path, '../..'))
from utils import load_data, execute_function

#% --------- THE IMPORTANT STUFF -------------

FILENAME = 'example_input.txt'
FILENAME = 'input.txt'
file_path = os.path.join(script_path, FILENAME)

def fits(key, lock):
    return all(k+l < 6 for k,l in zip(key, lock))

def parse_schematic(schematic: str) -> list[int]:
    object = [-1,]*5
    for row in schematic.split('\n'):
        for i,o in enumerate(row):
            if o=='#':
                object[i]+=1
    return object


def task_1():
    schematics = load_data(file_path).strip().split('\n\n')
    keys = []
    locks = []
    for schem in schematics:
        if schem.startswith('#'):
            locks.append(parse_schematic(schem))
        else:
            keys.append(parse_schematic(schem))

    return sum(
        fits(lock,key)
        for lock in locks
        for key in keys
    )

def task_2():
    data = load_data(file_path)
    return



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
    