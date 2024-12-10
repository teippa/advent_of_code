# https://adventofcode.com/2024/day/10
#%% ----------- SETUP -------------------------
from typing import Generator
import os
from sys import path as SYSPATH

script_path = os.path.dirname(os.path.abspath(__file__))

SYSPATH.append(os.path.join(script_path, '..'))
from utils import load_data, execute_function

#%% --------- THE IMPORTANT STUFF -------------

FILENAME = 'example_input.txt'
FILENAME = 'input.txt'
file_path = os.path.join(script_path, FILENAME)



class Data:
    directions = ((-1,0), (0,1), (1,0), (0,-1)) # URDL
    def __init__(self):
        self.data = load_data(file_path, matrix=True, dtype=int)
    
    def __getitem__(self, 
                    position: tuple[int,int]
                    ) -> int:
        x, y = position
        if (x<0 or y<0):
            # Let's not have a packman map
            raise IndexError("Negative indexes are not allowed")
        return self.data[y][x]
    def __setitem__(self, 
                    position: tuple[int,int], 
                    value: int):
        x, y = position
        if (x<0 or y<0):
            # Let's not have a packman map
            raise IndexError("Negative indexes are not allowed")
        self.data[y][x] = value
    
    def get(self, 
            position: tuple[int,int], 
            default=None) -> int:
        x,y = position
        try:
            return self[x,y]
        except IndexError:
            return default
        
    def __repr__(self) -> str:
        return '\n'.join(
            ''.join(str(n) for n in row)
            for row in self.data
        )
    
    def find_all(self, 
                 value: int
                 ) -> Generator[tuple[int, int], None, None]:
        """ Find all positions that have a given value
        """
        return (
            (x, y)
            for y, row in enumerate(self.data)
            for x, cell in enumerate(row)
            if value == cell
        )
        
    def move_position(self, 
                      position: tuple[int,int], 
                      direction: tuple[int,int]
                      ) -> tuple[int,int]:
        """ Translate position towards a direction:
        """
        return (
            position[0] + direction[0],
            position[1] + direction[1]
        )
    
    def find_possible_directions(self, 
                                 position: tuple[int,int]
                                 ) -> Generator[tuple[int,int], None, None]:
        """ Translate position towards each of the defined directions:
            - up, right down, left
        """
        for d in self.directions:
            next_pos = self.move_position(position, d)
            if self.get(next_pos) is not None:
                yield next_pos
        
                
def task_1():
    """ - Start from height 0
        - Travel to directions where height increases by 1
        - Add peak (height 9) position to a set if found
    """
    data = Data()    
    
    n_trail_peaks = 0
    for start_position in data.find_all(0):
        # Search queue.
        trail_position_pool = set((start_position, ))
        # The trail peaks that are found
        end_positions = set()

        # Minor optimization, so that we do not travel the same path multiple times
        visited_positions = set() 
        
        while len(trail_position_pool):
            position = trail_position_pool.pop()
            visited_positions.add(position)
            current_height = data.get(position)
            for next_pos in data.find_possible_directions(position):
                if next_pos in visited_positions:
                    # We have been here before
                    continue
                next_height = data.get(next_pos)
                if next_height is None:
                    # Position out of bounds
                    continue
                elif next_height == (current_height + 1):
                    # Slope increases by 1
                    if next_height == 9:
                        # Found the peak
                        end_positions.add(next_pos)
                    else:
                        # Still on trail, add position to search queue
                        trail_position_pool.add(next_pos)
        n_trail_peaks += len(end_positions)
    
    return n_trail_peaks

def task_2():
    """ The main differences to task 1 are:
        - trail_position_pool is a list, not a set, because a branch
        that merges back to trail is a unique path
        - visited_positions set is removed for the same reason as above
    """
    data = Data()    
    
    n_trail_peaks = 0
    for start_position in data.find_all(0):
        # Position search queue
        trail_position_pool = [start_position, ]
        
        while len(trail_position_pool):
            position = trail_position_pool.pop()
            current_height = data.get(position)
            for next_pos in data.find_possible_directions(position):
                next_height = data.get(next_pos)
                if next_height is None:
                    # Out of bounds
                    continue
                elif next_height == current_height + 1:
                    # Properly steep slope
                    if next_height == 9:
                        # Found a peak
                        n_trail_peaks += 1
                    else:
                        # Continue searching
                        trail_position_pool.append(next_pos)
    
    return n_trail_peaks



#% -------------------------------------------

if __name__ == "__main__":
    do_timing = True
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
# 	Result: 737
# 	Average exec time: 50.5278 ms.
# Function: task_2
# 	Result: 1619
# 	Average exec time: 74.3246 ms.
