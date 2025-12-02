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

class Wheel:
    size = 100
    _position = 50
    n_end_position_zero = 0
    n_visited_zero = 0
    def __init__(self):
        pass
    
    @property
    def position(self):
        """The wheel position property."""
        return self._position
    @position.setter
    def position(self, value):
        self._position = value % self.size
        # Count how many times we end up at zero
        if self._position == 0:
            self.n_end_position_zero += 1
    
    def rotate_wheel(self, amount: int, reverse: bool):
        if amount==0:
            return
        
        if n_full_rotates := amount // self.size:
            # We visit zero on every full rotation, so let's count them
            self.n_visited_zero += n_full_rotates
        
        # Calc is short for calculation, and that is what we are doing here.
        rotation = (-1 if reverse else 1) * (amount % self.size)
        overflow_position = self.position + rotation
        if self.position != 0 and not (0 < overflow_position < self.size):
            # If we end up beyond the wheel values, we have gone beyond zero.
            self.n_visited_zero += 1
            
        # Position setter handles the overflow with modulo
        self.position = overflow_position
        
    def do_instruction(self, instruction: str):
        direction = instruction[0]
        amount = int(instruction[1:])
                
        self.rotate_wheel(amount, direction == 'L')
        

    def __repr__(self):
        return f"{self.__class__.__name__}({self.position})"


def task_1():
    data = load_data(file_path, lines=True)
    wheel = Wheel()
    for row in data:
        wheel.do_instruction(row)
    return wheel.n_end_position_zero

def task_2():
    data = load_data(file_path, lines=True)
    wheel = Wheel()
    for row in data:
        wheel.do_instruction(row)
    return wheel.n_visited_zero



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
    
#%%

# Function: task_1()
#     Result: 1132
#     Execution time: 14.0026 ms.
# Function: task_2()
#     Result: 6623
#     Execution time: 16.4523 ms.