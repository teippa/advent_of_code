#%% ----------- SETUP -------------------------
import os
import sys

script_path = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_path, '..', '..'))

sys.path.append(project_root)
from utils import load_data, execute_function

#%% --------- THE IMPORTANT STUFF -------------



def task_1(input_path: str):
    data = load_data(input_path)
    return 

def task_2(input_path: str):
    data = load_data(input_path)
    return



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
            solution = None
        )
        task_2_success = execute_function(
            task_2,
            args = {'input_path': file_path_example},
            do_timing = do_timing,
            solution = None
        )
    
        file_path = os.path.join(script_path, 'input.txt')
        if os.path.isfile(file_path):
            print(f"Task with real inputs:")
            if task_1_success:
                execute_function(
                    task_1,
                    args = {'input_path': file_path},
                    do_timing = do_timing,
                    solution = None
                )
            if task_2_success:
                execute_function(
                    task_2,
                    args = {'input_path': file_path},
                    do_timing = do_timing,
                    solution = None
                )
        