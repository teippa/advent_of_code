# https://adventofcode.com/2025/day/3

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

def find_small_jolts(d: list[int]) -> int:
    tens = max(d[:-1])
    i = d.index(tens)
    ones = max(d[i+1:])
    return 10*tens + ones

def find_bigger(arr: list[int], ref: int) -> tuple[int, int]:
    for i, val in enumerate(arr[::-1], start=1):
        if val >= ref:
            return val, len(arr)-i
    return None, None

def find_removal(arr: list[int]) -> tuple[int, int]:
    for i, val in enumerate(arr[:-1]):
        if val < arr[i+1]:
            return val, i
    smallest = min(arr)
    return smallest, arr.index(smallest)

def find_big_jolts(d: list[int], n: int = 12) -> int:
    cursor = len(d) - n
    res = d[cursor:]
    while True:
        addition, add_i = find_bigger(d[:cursor], res[0])
        if add_i is None:
            break
        _, rem_i = find_removal(res)
        del res[rem_i]
        res.insert(0, addition)
        cursor = add_i
    return int(''.join(map(str, res)))

def task_1():
    data: list[list[int]] = load_data(file_path, matrix=True, dtype=int)
    jolts = map(find_small_jolts, data)
    return sum(jolts)

def task_2():
    data = load_data(file_path, matrix=True, dtype=int)
    jolts = list(map(find_big_jolts, data))
    return sum(jolts)


#% -------------------------------------------

if __name__ == "__main__":
    do_timing = False
    execute_function(
        task_1,
        args = {},
        do_timing = do_timing,
        solution = 17432 # 357 #
    )
    
    execute_function(
        task_2,
        args = {},
        do_timing = do_timing,
        solution = 173065202451341 # 3121910778619 #
    )
    