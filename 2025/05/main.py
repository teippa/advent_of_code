# https://adventofcode.com/2025/day/5

#%% ----------- SETUP -------------------------
import os
import sys

script_path = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_path, '..', '..'))

sys.path.append(project_root)
from utils import load_data, execute_function

#%% --------- THE IMPORTANT STUFF -------------


Produce = list[int]
Ranges = list[tuple[int,int]]

def is_within(value: int, check_range: tuple[int, int]) -> bool:
    return check_range[0] <= value <= check_range[1]

def compress_ranges(ranges: Ranges) -> Ranges:
    """
    Combine overlapping ranges
    """
    ranges.sort()
    compressed = []
    for r in ranges:
        for i, c in enumerate(compressed):
            if any(is_within(v, c) for v in r):
                compressed[i] = (min(r[0], c[0]), max(r[1], c[1]))
                break
        else:
            compressed.append(r)
    
    if len(compressed) < len(ranges):
        return compress_ranges(compressed)
    return compressed

def parse_data(raw_data: list[str]):
    ranges = []
    produce = []
    for line in raw_data:
        if not line:
            break
        ranges.append(tuple(map(int, line.split('-'))))
        
    produce = list(map(int, raw_data[len(ranges)+1:]))
    compressed = compress_ranges(ranges)
    
    return compressed, produce
    


def task_1(input_path: str):
    data = load_data(input_path, lines=True, dtype=str.strip)
    ranges, produce = parse_data(data)
    good_produce = [
        p
        for p in produce
        if any(is_within(p, r) for r in ranges)
    ]
    
    return len(good_produce)

def task_2(input_path: str):
    data = load_data(input_path, lines=True, dtype=str.strip)
    ranges, _ = parse_data(data)
    return sum(r[1] - r[0] + 1 for r in ranges)



#% -------------------------------------------

if __name__ == "__main__":
    do_timing = False
    
    file_path_example = os.path.join(script_path, 'example_input.txt')
    if os.path.isfile(file_path_example):
        print(f"Task with example inputs:")
        execute_function(
            task_1,
            args = {'input_path': file_path_example},
            do_timing = do_timing,
            solution = 3
        )
        
        execute_function(
            task_2,
            args = {'input_path': file_path_example},
            do_timing = do_timing,
            solution = 14
        )
    else:
        print(f"File {file_path_example} not found!")
    
    file_path = os.path.join(script_path, 'input.txt')
    if os.path.isfile(file_path):
        print(f"Task with real inputs:")
        execute_function(
            task_1,
            args = {'input_path': file_path},
            do_timing = do_timing,
            solution = 739
        )
        
        execute_function(
            task_2,
            args = {'input_path': file_path},
            do_timing = do_timing,
            solution = 344486348901788
        )
    else:
        print(f"File {file_path} not found!")

# Task with example inputs:
# Function: task_1
# 	Result: 3
# 	Execution time: 0.0000 ms.
# 	✔️ CORRECT!
# Function: task_2
# 	Result: 14
# 	Execution time: 0.0000 ms.
# 	✔️ CORRECT!
# Task with real inputs:
# Function: task_1
# 	Result: 739
# 	Execution time: 57.3697 ms.
# 	✔️ CORRECT!
# Function: task_2
# 	Result: 344486348901788
# 	Execution time: 17.5636 ms.
# 	✔️ CORRECT!
