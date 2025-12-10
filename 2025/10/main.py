# https://adventofcode.com/2025/day/10

#%% ----------- SETUP -------------------------
from collections import Counter, defaultdict
import os
from pprint import pprint
import random
import re
import sys

from tqdm import tqdm


script_path = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_path, '..', '..'))

sys.path.append(project_root)
from utils import load_data, execute_function

#%% --------- THE IMPORTANT STUFF -------------

def split_to_ints(value: str) -> tuple[int]:
    return tuple(map(int, value.split(',')))

def button_press_iterator(n):
    """  Generate button presses so that we toggle through all possible light states """
    if n == 0:
        return
    for p in button_press_iterator(n-1):
        yield p
    yield n-1
    for p in button_press_iterator(n-1):
        yield p

class Machine:
    def __init__(self, description: str):
        try:
            self.target_lights = int(re.match('\[(.+)\]', description)[1].replace('.', '0').replace('#', '1')[::-1], 2)
            self.buttons = tuple(
                set(int(i) for i in data[1].split(','))
                for data in re.finditer('\((.+?)\)', description)
            )
            self.wires = tuple(
                sum(2**int(i) for i in btn)
                for btn in self.buttons
            )
            self.target_joltages = split_to_ints(re.search('\{(.+)\}', description)[1])
            self.joltages = [0,]*len(self.target_joltages)
        except TypeError as e:
            print("MACHINE PARSING FAILED: {e}")
        self.reset()
            
    def __repr__(self):
        return f"Machine(running: {self.running})"
    
    def reset(self):
        self.button_log = defaultdict(int)
        self.joltages = [0,]*len(self.target_joltages)
        self.lights = 0

    def _toggle_light(self, light_index: int):
        self.lights[light_index] ^= 2**light_index
        
    @property
    def running(self) -> bool:
        return self.target_lights == self.lights
    
    def joltage_analysis(self) -> bool:
        return tuple(j_tgt - j for j_tgt, j in zip(self.target_joltages, self.joltages))
    
    @property
    def len_buttons(self) -> int:
        return len(self.buttons)
    
    def press_button(self, button_index: int, unpress: bool = False):
        if button_index >= self.len_buttons:
            raise ValueError("Button index out of range")
            
        self.lights ^= self.wires[button_index]
        
        N = -1 if unpress else 1
            
        self.button_log[button_index] += N
        for wire in self.buttons[button_index]:
            self.joltages[wire] += N

    def mash_all_the_buttons(self):
        solutions = []
        for btn_i in button_press_iterator(self.len_buttons):
            self.press_button(btn_i)
            
            if self.running:
                solutions.append({
                btn: n%2
                for btn, n in self.button_log.items()
                if n%2
            })
        
        return min(sum(sol.values()) for sol in solutions)
    
    def mash_random_buttons(self):
        wire_2_btn = defaultdict(list)
        for btn_i, btn in enumerate(self.buttons):
            for wire in  btn:
                wire_2_btn[wire].append(btn_i)
        solutions = []
        
        for _ in range(50):
            self.reset()
            while True:
                btn_index = random.randint(0, self.len_buttons-1)
                self.press_button(btn_index)
                joltage_diffs = self.joltage_analysis()
                if all(jd == 0 for jd in joltage_diffs):
                    print(joltage_diffs, list(self.button_log.values()))
                    if all(v>0 for v in self.button_log.values()):
                        solutions.append(sum(self.button_log.values()))
                        break
                
                
                if any(v<0 for v in self.button_log.values()):
                    press_i = min(self.button_log.items(), key = lambda x: x[1])[0]
                    self.press_button(press_i)
                elif random.random() > .1:
                    greatest_joltage_diff = max(enumerate(joltage_diffs), key=lambda x: abs(x[1]))[0]
                    self.press_button(
                        random.choice(wire_2_btn[greatest_joltage_diff]),
                        unpress=joltage_diffs[greatest_joltage_diff]<0
                    )
                else:
                    self.press_button(
                        int(max(self.button_log.items(), key=lambda x: x[1])[0]),
                        unpress=True
                    )
                
                
                if min(self.button_log.values()) < -5:
                    self.reset()
                    
                # over_joltages = tuple(i for i, jd in enumerate(joltage_diffs) if jd > 0)
                # if len(over_joltages):
                #     self.press_button(
                #         random.choice(wire_2_btn[random.choice(over_joltages)]),
                #         unpress=True
                #     )
                #     continue
                # under_joltages = tuple(i for i, jd in enumerate(joltage_diffs) if jd < 0)
                # if len(under_joltages):
                #     self.press_button(
                #         random.choice(wire_2_btn[random.choice(under_joltages)])
                #     )
                #     continue
                
                    
        
        return min(solutions)
            

def task_1(input_path: str):
    data = load_data(input_path, lines=True, dtype=Machine)
    return sum(d.mash_all_the_buttons() for d in data)

def wolfram_solve(d) -> str:
    vars = tuple('abcdefghijklmn'[:len(d.buttons)])
    left_side = ['',]*len(d.target_joltages)
    for i, btn in enumerate(d.buttons):
        for wire in btn:
            left_side[wire] += vars[i]
    
    all_eqn = "Solve["
    for i, row in enumerate(left_side):
        eqn = ' + '.join(row) + ' == ' + str(d.target_joltages[i])
        all_eqn += eqn + ', '
    # print(all_eqn)
    all_eqn += ', '.join(f'{v} >= 0' for v in vars)
    all_eqn += ', {' + ','.join(vars) + '}]'
    return all_eqn

def task_2(input_path: str):
    data = load_data(input_path, lines=True, dtype=Machine)
    return sum(
        d.mash_random_buttons()
        for d in tqdm(data)
    )



if __name__ == "__main__":
    do_timing = False
    
    file_path_example = os.path.join(script_path, 'example_input.txt')
    if os.path.isfile(file_path_example):
        print(f"Task with example inputs:")
        task_1_success = execute_function(
            task_1,
            args = {'input_path': file_path_example},
            do_timing = do_timing,
            solution = 7
        )
        task_2_success = execute_function(
            task_2,
            args = {'input_path': file_path_example},
            do_timing = do_timing,
            solution = 33
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
