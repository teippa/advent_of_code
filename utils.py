#%%
from timeit import timeit
from time import time
from functools import partial
from typing import Callable, Literal, TypeVar, overload

T = TypeVar('T')


@overload
def load_data(file_path: str, *,
              lines: False = ..., matrix: False = ...,
              dtype: Callable[[str], T] = ...
              ) -> str: ...

@overload
def load_data(file_path: str, *,
              lines: bool = Literal[True],
              dtype: Callable[[str], T] = ...
              ) -> list[T]: ...

@overload
def load_data(file_path: str, *, 
              matrix: bool = Literal[True],
              dtype: Callable[[str], T] = ... 
              ) -> list[list[T]]: ...

def load_data(file_path: str, 
              lines: bool = False, 
              matrix: bool = False,
              dtype: Callable[[str], T] = str):
    
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

def measure_execution_time(func: Callable, iterations: int = 100) -> float:
    execution_time = timeit(func, number=iterations)
    avg_time_per_call = execution_time / iterations

    return avg_time_per_call

def calculate_timeit_iterations(one_iteration_time_s: int, max_time_s: int = 30):
    if one_iteration_time_s < 0.01:
        return 10_000
    return max(1, int(max_time_s/one_iteration_time_s))

def execute_function(func: Callable, 
                     args: dict = None,
                     do_timing: bool = False, 
                     timeit_iterations: int = -1,
                     solution = None):
    if args is None: args = {}
    
    # Timing the first execution to calculate a good
    # number of timing iterations if not specified
    t0 = time() 
    result = func(**args)
    t_exec = time() - t0
    
    if do_timing:
        if timeit_iterations < 1:
            timeit_iterations = calculate_timeit_iterations(t_exec)
        partial_func = partial(func, **args)
        t_exec = measure_execution_time(partial_func, iterations=timeit_iterations)
    
    args_print = '(' + ', '.join(f"{k}={v!r}" for k,v in args.items()) + ')'
    print(f"Function: {func.__name__}" + args_print)
    print(f"\tResult: {result}")
    
    timing_text = 'Average exec time' if (do_timing and timeit_iterations>1) else 'Execution time'
    if t_exec > 1:
        print(f"\t{timing_text}: {t_exec:.4f} s.")
    else:
        print(f"\t{timing_text}: {1000*t_exec:.4f} ms.")
    
    if solution is not None:
        print("\t✔️ CORRECT!" if result == solution else "\t❌ INCORRECT!")
        
    return result

if __name__ == "__main__":
    def test(sleep_time):
        from time import sleep
        sleep(sleep_time)
        return "Success"

    execute_function(
        test, 
        args = {'sleep_time': .02}, 
        do_timing = True,
        timeit_iterations=500
    )