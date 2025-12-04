# https://adventofcode.com/2025/day/4

#%% ----------- SETUP -------------------------
import os
from pprint import pprint
from sys import path as SYSPATH

script_path = os.path.dirname(os.path.abspath(__file__))

SYSPATH.append(os.path.join(script_path, '../..'))
from utils import load_data, execute_function

#%% --------- THE IMPORTANT STUFF -------------

FILENAME = 'example_input.txt'
FILENAME = 'input.txt'
file_path = os.path.join(script_path, FILENAME)

def pad_0(data: list[list[int]]) -> list[list[int]]:
    padded = [
        [0,]*(len(data[0]) + 2),
        *([0, *row, 0] for row in data),
        [0,]*(len(data[0]) + 2)
    ]
    return padded

def remove_rolls(data):
    accessible_rolls = 0
    padded_data = pad_0(data)
    kernel = [
        [1, 1, 1],
        [1, 0, 1],
        [1, 1, 1],
    ]
    for i, row in enumerate(data):
        for j, cell in enumerate(row):
            if not cell:
                continue
            selection = [
                [
                    x*kernel[ii][jj] 
                    for jj, x in enumerate(xx[j:j+3])
                ]
                for ii, xx in enumerate(padded_data[i:i+3])
            ]
            if sum(sum(row) for row in selection) < 4:
                data[i][j] = 0
                accessible_rolls += 1
    return data, accessible_rolls

def task_1():
    data = load_data(file_path, matrix=True, dtype=lambda x: int(x=='@'))
    _, n_rolls = remove_rolls(data)
    return n_rolls

def task_2():
    data = load_data(file_path, matrix=True, dtype=lambda x: int(x=='@'))
    n_removed_total = 0
    while True:
        data, n_removed = remove_rolls(data)
        if n_removed == 0:
            break
        n_removed_total += n_removed
    return n_removed_total



#% -------------------------------------------

if __name__ == "__main__":
    do_timing = False
    execute_function(
        task_1,
        args = {},
        do_timing = do_timing,
        solution = 1389 # 13 #
    )
    
    execute_function(
        task_2,
        args = {},
        do_timing = do_timing
    )
    