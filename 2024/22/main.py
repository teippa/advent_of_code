# https://adventofcode.com/2024/day/22
#%% ----------- SETUP -------------------------
from collections import Counter
from functools import lru_cache
from itertools import islice, repeat
import os
from sys import path as SYSPATH
from typing import Generator
from tqdm import tqdm

script_path = os.path.dirname(os.path.abspath(__file__))

SYSPATH.append(os.path.join(script_path, '..'))
from utils import load_data, execute_function

#% --------- THE IMPORTANT STUFF -------------

FILENAME = 'example_input.txt'
FILENAME = 'input.txt'
file_path = os.path.join(script_path, FILENAME)


def mix(value, sn):
    return value ^sn

def prune(sn):
    return sn % 16777216


def generate_secret_numbers(initial_number: int) -> Generator[int, None, None]:
    sn = initial_number
    while True:
        sn  = prune(mix(sn * 64, sn))
        sn  = prune(mix(sn // 32, sn))
        sn  = prune(mix(sn * 2048, sn))
        yield sn

@lru_cache(maxsize=5_000)
def losn(sn0):
    return tuple(islice(generate_secret_numbers(sn0), 2000))

def task_1():
    secret_numbers = load_data(file_path, lines=True, dtype=int)

    return sum(
        losn(sn)[-1]
        for sn in secret_numbers
    )

def diff(arr):
    return (
        b-a
        for a, b in zip(arr[:-1], arr[1:])
    )


def task_2():
    secret_numbers = load_data(file_path, lines=True, dtype=int)
    # print(len(secret_numbers))
    
    vendors_prices = tuple(
        tuple(
            int(str(sn)[-1])
            for sn in losn(sn0)
        )
        for sn0 in secret_numbers
    )

    vendors_price_diffs = tuple(
        tuple(diff(pl))
        for pl in vendors_prices
    )

    kaikkivitunslaissit = [
        tuple(vpd[i:i+4])
        for vpd in vendors_price_diffs
        for i in range(len(vpd)-3)
    ]

    frequent_patterns = sorted(
        Counter(kaikkivitunslaissit).items(), 
        key=lambda x: -x[1]
    )

    def samesies(l1, l2):
        if len(l1) != len(l2):
            print(l1, l2)
            raise IndexError("asdasd")
        return all(a==b for a,b in zip(l1,l2))

    def findthefuckingthing(prices, diffs, pattern):
        LL = len(pattern)
        for iiiii in range(len(diffs)-LL):
            if samesies(diffs[iiiii:iiiii+LL], pattern):
                return prices[iiiii+LL]
            
    pattern_values = {}
    for fp, N in tqdm(frequent_patterns):
        try:
            pattern_value = 0
            for vp, vpd in zip(vendors_prices, vendors_price_diffs):
                thing = findthefuckingthing(
                    vp, 
                    vpd,
                    fp
                )
                if thing is not None:
                    pattern_value += thing
            pattern_values[fp] = pattern_value
        except KeyboardInterrupt:
            # Lets just stop at some point and hope for the best
            print("Interrupted at", fp, N)
            break

    for p, v in sorted(pattern_values.items(), key=lambda x: -x[1])[:20]:
        print(p, v)        



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
# 	Result: 18317943467
# 	Execution time: 4.7023 s.
#   1%|▏         | 519/40951 [5:40:58<442:43:33, 39.42s/it]  
# Interrupted at (-3, 2, -1, 1) 301
# (2, -2, 4, 0) 2018
# (-3, 2, 1, 0) 2007
# (0, -1, 2, 0) 1974
# (0, -1, 0, 2) 1964
# (1, 0, -2, 3) 1955
# (-1, 2, -2, 2) 1954
# (2, 1, -3, 3) 1939
# (-3, 3, 0, 0) 1938
# (-2, 1, -1, 2) 1935
# (1, -1, -1, 2) 1933
# (0, 0, 3, 0) 1923
# (0, 0, -1, 1) 1916
# (-3, 2, 0, 1) 1914
# (0, 1, 0, 0) 1909
# (-1, 0, 1, 0) 1900
# (-1, 1, 1, 0) 1889
# (-1, 0, 1, 1) 1888
# (-2, 2, -2, 3) 1886
# (1, -3, 3, 0) 1879
# (1, -1, 0, 1) 1878
# Function: task_2()
# 	Result: None
# 	Execution time: 20465.2318 s.