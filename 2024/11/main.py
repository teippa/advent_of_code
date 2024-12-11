# https://adventofcode.com/2024/day/11
#%% ----------- SETUP -------------------------
from collections import Counter, defaultdict
import os
from sys import path as SYSPATH

from functools import lru_cache
from typing import Iterable

script_path = os.path.dirname(os.path.abspath(__file__))

SYSPATH.append(os.path.join(script_path, '..'))
from utils import load_data, execute_function

#% --------- THE IMPORTANT STUFF -------------

FILENAME = 'example_input.txt'
FILENAME = 'input.txt'
file_path = os.path.join(script_path, FILENAME)


def splitter(value: int, split_index: int) -> tuple[int,int]:
    """ Split stone in half 123678 -> 123, 678
    """
    value_str = str(value)
    return (
        int(value_str[split_index:]),
        int(value_str[:split_index]) 
    )

@lru_cache(maxsize=10_000)
def transform(value: int) -> tuple[int]:
    """ The thing that happens to each stone after a blink
    """
    if value == 0:
        return (1, )
    length = len(str(value))
    if length % 2 == 0:
        return splitter(value, length//2)
    return (value*2024, )


def main(initial_stones: Iterable[int], n_blinks: int) -> int:
    # 'ORdEr iS pReSerVeD' - Yeah, sure...
    stones = Counter(initial_stones)
        
    for _ in range(n_blinks):
        created_stones = defaultdict(int)
        for stone in stones:
            for new_stone in transform(stone):
                created_stones[new_stone] += stones[stone]
        stones = created_stones
    
    return sum(stones.values())

    
def task_1():
    transform.cache_clear()
    data = map(int, load_data(file_path).strip().split())
    return main(data, 25)

def task_2():
    transform.cache_clear()
    data = map(int, load_data(file_path).strip().split())
    return main(data, 75)


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
    
# Function: task_1
# 	Result: 193607
# 	Average exec time: 5.5785 ms.
# Function: task_2
# 	Result: 229557103025807
# 	Average exec time: 126.3002 ms.
