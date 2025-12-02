#%% ----------- SETUP -------------------------
from itertools import product
import os
from sys import path as SYSPATH

script_path = os.path.dirname(os.path.abspath(__file__))

SYSPATH.append(os.path.join(script_path, '../..'))
from utils import load_data, execute_function

#%% --------- THE IMPORTANT STUFF -------------

FILENAME = 'example_input.txt'
FILENAME = 'input.txt'

# from operator import mul
# from functools import reduce

def load_to_dict(filename):
    file_path = os.path.join(script_path, filename)
    data = []
    with open(file_path, 'r') as file:
        for line in file.readlines():
            if len(line.strip()) == 0: continue
            ans, values_str = line.strip().split(':')
            values = tuple(
                int(val)
                for val in values_str.split(' ')
                if val
            )
            data.append( (int(ans), values) )
    return data

def task_1():
    # def answer_too_large(ans, nums):
    #     # This fails if all values are ones or something 
    #     return ans > reduce(mul, nums)

    # def answer_too_small(ans, nums):
    #     # This fails if all values are ones or something 
    #     return ans < sum(nums)

    def oddity_test_failed(ans, nums): 
        # if all values are even, answer should be even
        is_even = lambda x: x%2==0
        if not is_even(ans):
            return all(map(is_even, nums))
        return False
    
    equations = load_to_dict(FILENAME)
    
    eq_sum = 0
    for eq in equations:
        if oddity_test_failed(*eq):
            # This test makes the script marginally more
            # efficient, which is good enough for me
            continue
        ans, nums = eq
        
        # All possible ways of summing and multiplying values
        equation_operator_combinations = product(
            ['m', 's'], 
            repeat=len(nums)-1
        )
        for equation_operators in equation_operator_combinations:
            result = nums[0]
            for i, operator in enumerate(equation_operators, start=1):
                if result > ans: break
                if operator == 'm': # Multiply
                    result *= nums[i]
                if operator == 's': # Sum
                    result += nums[i]
            else:
                # Loop finished without break
                if result == ans:
                    eq_sum += ans
                    break
                
    return eq_sum

def task_2():
    from tqdm import tqdm
    equations = load_to_dict(FILENAME)
    
    eq_sum = 0
    for eq in tqdm(equations, desc="Analysing equations", ascii=' #'):
        ans, nums = eq
        calculation_combinations = product(
            ['m', 's', 'c'], 
            repeat=len(nums)-1
        )
        for calcs in calculation_combinations:
            result = nums[0]
            for i, calc in enumerate(calcs, start=1):
                if result > ans: break
                if calc == 'm': # Multiply
                    result *= nums[i]
                elif calc == 's': # Sum
                    result += nums[i]
                elif calc == 'c': # Concatenate
                    result = int(str(result)+str(nums[i]))
            else:
                # Loop finished without break
                if result == ans:
                    eq_sum += ans
                    break
    
    return eq_sum



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
    #     Result: 538191549061
    #     Execution time: 949.6558 ms.
    # Function: task_2
    #     Result: 34612812972206
    #     Execution time: 75.3674 s.

