# https://adventofcode.com/2025/day/9

#%% ----------- SETUP -------------------------
import os
import sys

script_path = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_path, '..', '..'))

sys.path.append(project_root)
from utils import load_data, execute_function

#%% --------- THE IMPORTANT STUFF -------------
from pprint import pprint

Point = tuple[int, int]

def split_and_cast(row: str) -> Point:
    return tuple(map(int, row.split(',') ))

def calc_area(corner_1: Point, corner_2: Point) -> int:
    return (abs(corner_1[0]-corner_2[0])+1)*(abs(corner_1[1]-corner_2[1])+1)

def task_1(input_path: str):
    data = load_data(input_path, lines=True, dtype=split_and_cast)
    
    areas = [
        calc_area(a, b)
        for i, a in enumerate(data[:-1])
        for b in data[i+1:]
    ]
    return max(areas)

def is_within_area(area: tuple[Point, Point], point: Point):
    sorted_corners_0 = sorted((area[0][0], area[1][0]))
    sorted_corners_1 = sorted((area[0][1], area[1][1]))
    between_0 = sorted_corners_0[0] < point[0] < sorted_corners_0[1]
    between_1 = sorted_corners_1[0] < point[1] < sorted_corners_1[1]
    return between_0 and between_1

def task_2(input_path: str):
    data = load_data(input_path, lines=True, dtype=split_and_cast)    
    
    areas = [
        calc_area(a, b)
        for i, a in enumerate(data[:-1])
        for b in data[i+1:]
        if not any(
            is_within_area((a,b), point)
            for point in data
        )
    ]
    return max(areas)



#% -------------------------------------------

if __name__ == "__main__":
    do_timing = False
    
    file_path_example = os.path.join(script_path, 'example_input.txt')
    if os.path.isfile(file_path_example):
        print(f"Task with example inputs:")
        task_1_success = execute_function(
            task_1,
            args = {'input_path': file_path_example},
            do_timing = do_timing,
            solution = 50
        )
        task_2_success = execute_function(
            task_2,
            args = {'input_path': file_path_example},
            do_timing = do_timing,
            solution = 24
        )
    
        file_path = os.path.join(script_path, 'input.txt')
        if os.path.isfile(file_path):
            print(f"Task with real inputs:")
            if task_1_success:
                execute_function(
                    task_1,
                    args = {'input_path': file_path},
                    do_timing = do_timing,
                    solution = 4763932976
                )
            if True:
                execute_function(
                    task_2,
                    args = {'input_path': file_path},
                    do_timing = do_timing,
                    solution = None
                )
