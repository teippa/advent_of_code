#%%
from os import path
from timeit import timeit

FILENAME = 'example_input.txt'
# FILENAME = 'input.txt'

def timing(fun: callable, n: int = 100) -> float:
    exec_time = timeit(fun, number=n)
    average_exec_ms = 1000*exec_time/n
    print(f"{fun.__name__} average exec time: {average_exec_ms:.4f} ms")
    return average_exec_ms

def load_data(filename: str, 
              lines: bool = False, 
              matrix: bool = False,
              dtype: callable = str):
    
    script_path = path.dirname(path.abspath(__file__))
    file_path = path.join(script_path, filename)
    
    with open(file_path, 'r', encoding='utf-8') as file:
        if matrix:
            return [
                [dtype(char) for char in line.strip()]
                for line in file.readlines()
            ]
        if lines:
            return [
                dtype(line)
                for line in file.readlines()
            ]
        return file.read()


def task_1():
    return

def task_2():
    return
    
if __name__ == "__main__":
    print('task_1:', task_1())

    # print('task_2:', task_2(data))
    
    # timing(task_1)
    # timing(task_2)
    