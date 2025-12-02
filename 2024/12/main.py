# https://adventofcode.com/2024/day/12
#%% ----------- SETUP -------------------------
from collections import defaultdict
import os
from pprint import pprint
from sys import path as SYSPATH

script_path = os.path.dirname(os.path.abspath(__file__))

SYSPATH.append(os.path.join(script_path, '../..'))
from utils import load_data, execute_function

#% --------- THE IMPORTANT STUFF -------------

from PotteryMap import PotteryMap
from RegionScanner import RegionScanner

FILENAME = 'example_input.txt'
FILENAME = 'input.txt'
# FILENAME = 'test_input.txt' # Test input, where the first area 'R' (index: 1) touches itself diagonally

file_path = os.path.join(script_path, FILENAME)



def task_1():
    def new_region():
        return {
            'area': 0,
            'perimeter': 0
        }
    data = load_data(file_path, matrix=True)
    pottery_map = PotteryMap(data)
    regions = defaultdict(new_region)
    
    for position, pot in pottery_map.iterate_pots():
        # Increase the area of this pot type
        regions[pot]['area'] += 1
        
        for pot_around in pottery_map.pots_around(position):
            # Look around the pot. If the surrounding pots are 
            # different types, there needs to be a fence there.
            if pot_around != pot:
                regions[pot]['perimeter'] += 1
    
    return sum(
        region['area'] * region['perimeter']
        for region in regions.values()
    )

def task_2():
    data = load_data(file_path, matrix=True)
    pottery_map = PotteryMap(data)

    total_cost = 0
    for region in pottery_map.regions:
        # Scan each region and count the cost
        scanner = RegionScanner(pottery_map.get_region_positions(region))
        total_cost += scanner.scan_region() * scanner.area

    return total_cost


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
# 	Result: 1374934
# 	Execution time: 61.8243 ms.
# Function: task_2()
# 	Result: 841078
# 	Execution time: 952.7192 ms.