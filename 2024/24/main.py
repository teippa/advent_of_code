# https://adventofcode.com/2024/day/24
#%% ----------- SETUP -------------------------
import os
import re
from sys import path as SYSPATH
from typing import Callable

script_path = os.path.dirname(os.path.abspath(__file__))

SYSPATH.append(os.path.join(script_path, '..'))
from utils import load_data, execute_function

#% --------- THE IMPORTANT STUFF -------------

FILENAME = 'example_input.txt'
FILENAME = 'input.txt'
file_path = os.path.join(script_path, FILENAME)


class Wire:
    name = ''
    _lambdaFun = None
    _lambdaResult = None
    def __init__(self, s: str):
        m = re.match(r'(.+): (\d+)', s)
        if m is not None:
            name, value = m.groups()
            self._lambdaResult = int(value)
            self.name = name
        else:
            m = re.match(r'(.+) (.+) (.+) -> (.+)', s)
            if m is not None:
                a, op, b, name = m.groups()
                self.name = name
                self._lambdaFun = lambda: OPERATORS[op](WIRES[a].value, WIRES[b].value)
            else:
                raise Exception("Bad pattern")
        
    @property
    def value(self):
        if self._lambdaResult is None:
            self._lambdaResult = self._lambdaFun()
        return self._lambdaResult

    def __repr__(self):
        return self.name
    


WIRES: dict[str, Wire] = {}
OPERATORS: dict[str, Callable[[int, int], int]] = {
    'AND': lambda a,b: a & b,
    'OR': lambda a,b: a | b,
    'XOR': lambda a,b: a ^ b,
}

def task_1():
    data = load_data(file_path)

    # Create wires
    for d in data.split('\n'):
        if not d.strip():
            continue
        w = Wire(d)
        WIRES[w.name] = w
    
    # Read wires
    binary = ''.join(
        str(w.value)
        for n, w in sorted(WIRES.items(), reverse=True)
        if n.startswith('z')
    )
    return int(binary, 2) 


def task_2():
    data = load_data(file_path)
    return



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
# 	Result: 59336987801432
# 	Execution time: 4.0073 ms.