#%% ----------- SETUP -------------------------
import os
from sys import path as SYSPATH

script_path = os.path.dirname(os.path.abspath(__file__))

SYSPATH.append(os.path.join(script_path, '../..'))
from utils import load_data, execute_function

#%% --------- THE IMPORTANT STUFF -------------

FILENAME = 'example_input.txt'
FILENAME = 'input.txt'
file_path = os.path.join(script_path, FILENAME)


def error_finder(id_range: list[str, str]):
    """
    There are only a few ids that have twice repeating digits, so let's 
    try to generate and test them...
    
    if we have range 1099-1300 we can cut the range end points in half:
        1099 -> 10 and 1300 -> 13
    then we can generate suggestions for possible repeating patterns:
        1010, 1111, 1212, 1313
    This gets a solution that is close to the correct one, but 1010 is 
    too small and 1313 is too large. They need to be filtered away.
    
    The first and last solutions need to always be checked, but every 
    value between them is guaranteed to be within the range.
        - 123*** is always larger than 122*** and smaller than 124***
        - 123*** may be larger or smaller than 123xxx
    
    Values that have odd numbered digits are a problem, but they can 
    just be removed from the range, because they can never have errors.
    """
    errors = []
    id_0_str, id_1_str = id_range
    
    pattern_len = len(id_0_str)
    id_0, id_1 = int(id_0_str), int(id_1_str)
    
    if pattern_len != len(id_1_str):
        # If the range spans multiple magnitudes, split it into multiple parts
        # 80-123 -> 80-99 & 100-123
        # Then run this function to each range separately.
        splitted_ranges = split_range(id_range)
        for new_range in splitted_ranges:
            errors.extend(error_finder(new_range))
        return errors
    
    # If the range values have odd number of digits, they are all correct 
    if pattern_len % 2 != 0:
        return []
    
    # Generate all possible repeating patterns somewhat within the range
    seed_length = pattern_len//2
    checks = list(
        int(2*str(seed))
        for seed in range(
            int(id_0_str[:seed_length]), 
            int(id_1_str[:seed_length])+1
        )
    )
    
    is_within_range = lambda chk: (id_0 <= chk <= id_1)
    
    # Test the first pattern
    if is_within_range(checks[0]):
        errors.append(checks[0])
    
    if len(checks) > 1:
        # Test the last pattern
        if is_within_range(checks[-1]):
            errors.append(checks[-1])
        
        if len(checks) > 2:
            # Add all patterns between
            errors.extend(checks[1:-1])
    return errors


def finder_i_barely_know_her(id_range: list[str, str]):
    """
    Similar to the error_finder logic above, but we need to generate 
    and test more numbers, and also include values with odd number of 
    digits.
    
    With range from the example in `error_finder` 1099-1300 we can 
    create the required test values:
        1111, (One value repeating 4 times) 
        1010, 1111, 1212, 1313 (Two values repeating 2 times)
    then we just test if these are within the range
    """
    errors = set()
    id_0_str, id_1_str = id_range
    
    pattern_len = len(id_0_str)
    id_0, id_1 = int(id_0_str), int(id_1_str)
    
    if pattern_len != len(id_1_str):
        # If the range spans multiple magnitudes, split it into multiple parts
        # 80-123 -> 80-99 & 100-123
        # Then run this function to each range separately.
        splitted_ranges = split_range(id_range)
        for new_range in splitted_ranges:
            errors.update(finder_i_barely_know_her(new_range))
        return errors
    
    # Seed lengths range from 1 up to half of the pattern length
    for seed_len in range(1, (pattern_len//2)+1):
        # Generate seeds within the range values
        seeds = map(str, range(
            int(id_0_str[:seed_len]), 
            int(id_1_str[:seed_len])+1
        ))
        for seed in seeds:
            # Repeat seed N times to form a test ID and try if it is within the range
            rep_n = (pattern_len//len(seed))
            if rep_n > 1:
                check_id_0 = int(seed * rep_n)
                if id_0 <= check_id_0 <= id_1:
                    errors.add(check_id_0)
            
    return errors

def split_range(id_range):
    """
    Split id range into parts if it spans multiple orders of magnitude.
    This makes the problem easier because all values within a range have
    the same number of digits.
    """
    id_0, id_1 = id_range
    
    len_diff = len(id_1) - len(id_0)
    if len_diff == 0:
        return [id_range, ]
    elif len_diff == 1:
        # Split range into two parts
        # For example: 80-123 -> 80-99 & 100-123
        return [
            [id_0, '9'*len(id_0)],
            ['1' + '0'*(len(id_1)-1), id_1]
        ]
    else:
        # Let's hope there are no massive ranges, like 123-12345, so that life is easier.
        raise ValueError("TOO LARGE RANGE! NOT IMPLEMENTED TO HANDLE THIS!!")
    
    
def sum_results(results: list) -> int:
    return sum(sum(errs) for errs in results)


def task_1():
    data = load_data(file_path, lines=True)
    id_ranges = [
        [
            id_value.strip()
            for id_value in id_range.split('-')
        ]
        for id_range in data[0].split(',')
    ]
    errors = map(error_finder, id_ranges)
    return sum_results(errors)

def task_2():
    data = load_data(file_path, lines=True)
    id_ranges = [
        [
            id_value.strip()
            for id_value in id_range.split('-')
        ]
        for id_range in data[0].split(',')
    ]
    errors = map(finder_i_barely_know_her, id_ranges)
    return sum_results(errors)


#% -------------------------------------------

if __name__ == "__main__":
    do_timing = False
    execute_function(
        task_1,
        args = {},
        do_timing = do_timing,
        solution = 56660955519
    )
    
    execute_function(
        task_2,
        args = {},
        do_timing = do_timing,
        solution = 79183223243
    )
    
#%%

