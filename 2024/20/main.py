# https://adventofcode.com/2024/day/20
#%% ----------- SETUP -------------------------
from collections import Counter
import importlib
import os
from sys import path as SYSPATH
from typing import Generator

script_path = os.path.dirname(os.path.abspath(__file__))

SYSPATH.append(os.path.join(script_path, '../..'))
from utils import load_data, execute_function

#% --------- THE IMPORTANT STUFF -------------

FILENAME = 'example_input.txt'
FILENAME = 'input.txt'
file_path = os.path.join(script_path, FILENAME)

import race_map
try:
    # Reload the modules to reflect changes
    importlib.reload(race_map)
except ImportError as e:
    print(e)


def print_time_saves(time_saves: Counter):
    for k, v in time_saves.items():
        if v>1:
            print(f"There are {v} cheats that save {k} picoseconds.")
        else:
            print(f"There is one cheat that saves {k} picoseconds.")


def get_scan_kernel(cheat_length, vis = False) -> list[race_map.Coordinate]:
    n = cheat_length+1
    a = []
    for i in range(-n,n):
        w = n-abs(i)-1
        if vis:
            print((n-w) * '  ', end='')

        for j in range(-w,w+1):
            if i!=0 or j!=0:
                a.append(race_map.Coordinate(j,i))
                if vis:
                    print('X ', end='')
            elif vis:
                print('  ', end='')
        if vis:
            print()
    return a

def scan_cheating_time_saves(rm, scan_kernel) -> Generator[int, None, None]:
    for pos, pos_distance in rm.distances.items():
        # Get all positions in range around this point
        cheat_endpoints = (
            (pos + scan_translation, scan_translation.manhattan_distance)
            for scan_translation in scan_kernel
        )
        # Filter out walls (and positions outside map)
        filtered_cheat_endpoints = (
            (cep, cep_distance)
            for cep, cep_distance in cheat_endpoints
            if rm.data.is_on_path(cep) 
        )
        # Calculate benefits of cheating to the positions
        cheat_benefits = (
            pos_distance - rm.distances[fcep] - fcep_distance
            for fcep, fcep_distance in filtered_cheat_endpoints
        )
        
        for time_benefit in cheat_benefits:
            if time_benefit>0:
                yield time_benefit
    
def task_1():
    data = load_data(file_path)
    rm = race_map.RaceMap(data)
    rm.calculate_paths()
    # print(rm)

    scan_kernel: list[race_map.Coordinate] = get_scan_kernel(2)
    
    all_time_saves_that_are_good_enough = (
        time_save
        for time_save in scan_cheating_time_saves(rm, scan_kernel)
        if time_save >= 100
    )
    
    counted_time_saves = Counter(all_time_saves_that_are_good_enough)
    
    # print_time_saves(counted_time_saves)
    return sum(counted_time_saves.values())

def task_2():
    data = load_data(file_path)
    rm = race_map.RaceMap(data)
    rm.calculate_paths()
    
    scan_kernel: list[race_map.Coordinate] = get_scan_kernel(20)
    
    all_time_saves_that_are_good_enough = (
        time_save
        for time_save in scan_cheating_time_saves(rm, scan_kernel)
        if time_save >= 100
    )
    
    counted_time_saves = Counter(all_time_saves_that_are_good_enough)
    
    # print_time_saves(counted_time_saves)
    return sum(counted_time_saves.values())
    



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
# 	Result: 1323
# 	Execution time: 953.9285 ms.
# Function: task_2()
# 	Result: 983905
# 	Execution time: 29.6674 s.