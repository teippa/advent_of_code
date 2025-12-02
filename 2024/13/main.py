# https://adventofcode.com/2024/day/13
#%% ----------- SETUP -------------------------
from dataclasses import dataclass
import os
from sys import path as SYSPATH

script_path = os.path.dirname(os.path.abspath(__file__))

SYSPATH.append(os.path.join(script_path, '../..'))
from utils import load_data, execute_function

#%% --------- THE IMPORTANT STUFF -------------

FILENAME = 'example_input.txt'
FILENAME = 'input.txt'
file_path = os.path.join(script_path, FILENAME)
import re

from decimal import Decimal

def this_is_integer(value):
    # This stuff is fine, I promise
    try:
        return float.is_integer(value)
    except TypeError:
        # This is for Decimal type, since it fails on float test
        return '.' not in str(value)

def data(multiply: bool = False):
    for d in load_data(file_path).split('\n\n'):
        values = [Decimal(x) for x in re.findall(r'[XY]\+?(-?\d+)', d)]
        targets = [Decimal(x) for x in re.findall(r'[XY]=(-?\d+)', d)]
        vars = {
            'x1': values[0],
            'y1': values[1],
            'x2': values[2],
            'y2': values[3],
            'r1': targets[0] + multiply * Decimal(1e13),
            'r2': targets[1] + multiply * Decimal(1e13),
        }
        yield vars

def do_the_cost_calculation(d):
    a_top = d['r2']*d['x2'] - d['y2']*d['r1']
    a_bot = d['x2']*d['y1'] - d['y2']*d['x1']
    a = a_top / a_bot

    b = (d['r1'] - d['x1']*a) / d['x2'] # Let's hope there's no floating point errors
    cost = a*3 + b

    # print(cost)
    if this_is_integer(cost):
        return cost
    return 0



def task_1():
    return int(sum(map(do_the_cost_calculation, data())))

def task_2():
    return int(sum(map(do_the_cost_calculation, data(multiply=True))))



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
# 	Result: 29438
# 	Execution time: 2.5034 ms.
# Function: task_2()
# 	Result: 104958599303720
# 	Execution time: 2.0039 ms.
