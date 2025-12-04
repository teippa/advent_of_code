#%% ----------- SETUP -------------------------
import os
from sys import path as SYSPATH

script_path = os.path.dirname(os.path.abspath(__file__))

SYSPATH.append(os.path.join(script_path, '../..'))
from utils import load_data, execute_function

#%% --------- THE IMPORTANT STUFF -------------

FILENAME = 'example_input.txt'
# FILENAME = 'input.txt'
file_path = os.path.join(script_path, FILENAME)



def task_1():
    data = load_data(file_path)
    return 

def task_2():
    data = load_data(file_path)
    return



#% -------------------------------------------

if __name__ == "__main__":
    do_timing = False
    execute_function(
        task_1,
        args = {},
        do_timing = do_timing,
        solution = None
    )
    
    execute_function(
        task_2,
        args = {},
        do_timing = do_timing,
        solution = None
    )
    