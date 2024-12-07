#%% ----------- SETUP -------------------------
import os
from sys import path as SYSPATH

script_path = os.path.dirname(os.path.abspath(__file__))

SYSPATH.append(os.path.join(script_path, '..'))
from utils import load_data, execute_function

#%% --------- THE IMPORTANT STUFF -------------
FILENAME = 'example_input.txt'
FILENAME = 'input.txt'

class GuardMap:
    directions = ((0, -1), (1, 0), (0, 1), (-1, 0)) #URDL
    rotate_history: set[tuple[int, int, int]] = None # set definition must be in __init__ ('mutable default argument pitfall')
    looping = False
    def __init__(self, filename, custom_obstacle_position: tuple[int,int]|None = None):
        self.data = self._load_data(filename)
        self._direction_index = 0
        self.rotate_history = set()
        self.position = self._find_starting_position()
        
        # Set obstacle somewhere, if defined
        if custom_obstacle_position and not self.is_same_position(self.position, custom_obstacle_position):
            self.try_set(*custom_obstacle_position, 0)
        
    def _load_data(self, filename: str) -> tuple[tuple[int]]:
        file_path = os.path.join(script_path, filename)
        def str2int(s):
            if s == '#': return 0 # Obstacles are 0
            elif s == '.': return -1 # Empty space is negative
            elif s == '^': return 1 # Footprints are 1,2,3,4 (all directions)
            else: raise Exception('Invalid character in map.')
        return load_data(
            file_path, 
            matrix=True,
            dtype=str2int
        )
        
    def is_same_position(self, pos_1: tuple[int,int], pos_2: tuple[int,int]) -> bool:
        return all(p1==p2 for p1,p2 in zip(pos_1, pos_2))
    
    def i_have_rotated_here_before(self):
        my_state = (*self.position, self._direction_index)
        return any(
            all(a==b for a,b in zip(my_state, history_node))
            for history_node in self.rotate_history
        )
        
    
    def rotate_direction(self):
        if self.i_have_rotated_here_before():
            self.looping = True
        self.rotate_history.add((*self.position, self._direction_index))
        self._direction_index = (self._direction_index + 1)%len(self.directions)
        self.previous_rotate = self.position
    
    @property
    def direction(self) -> tuple[int,int]:
        return self.directions[self._direction_index]
    
    def _find_starting_position(self):
        for y, row in enumerate(self.data):
            try:
                return (row.index(1), y)
            except ValueError:
                continue
        raise ValueError("Position not found!")
    
        
    def __getitem__(self, position: tuple[int,int]) -> int:
        x, y = position
        try:
            return self.data[y][x]
        except IndexError:
            return None
    def __setitem__(self, position: tuple[int,int], value: int) -> bool:
        x, y = position
        self.data[y][x] = value
    
    def try_get(self, x: int, y: int, default: int|None = None) -> int:
        try:
            return self[x, y]
        except IndexError:
            return default
        
    def try_set(self, x: int, y: int, value) -> bool:
        try:
            self[x, y] = value
            return True
        except IndexError:
            return False
        
    def is_occupied(self, x: int, y: int) -> bool:
        return self[x, y] == 0
    
    def _is_in_bounds(self, x: int, y: int) -> bool:
        """ Checks if the coordinates are within data bounds
        """
        ob_x, ob_y = self.shape
        return (0 <= x < ob_x) and (0 <= y < ob_y)
    
    @property
    def shape(self) -> tuple[int,int]:
        y = len(self.data)
        x = 0 if y==0 else len(self.data[0])
        return (x, y)
    
    def __repr__(self) -> str:
        chars = '#^>v<????.'
        return '\n'.join((
            ''.join(chars[i] for i in row)
            for row in self.data
        ))
        
    
    @staticmethod
    def translate_position(position: tuple[int,int], direction: tuple[int,int]) -> tuple[int,int]:
        return tuple(map(sum, zip(position, direction)))
    
    def add_footprint(self) -> bool:
        return self.try_set(*self.position, self._direction_index+1)
        
    def travel(self) -> bool:
        next_pos = None
        for _ in range(4):
            next_pos = self.translate_position(
                self.position,
                self.direction
            )
            if not self.is_occupied(*next_pos):
                break
            self.rotate_direction()
            
        
        self.position = next_pos
        position_in_bounds = self.add_footprint()
        return position_in_bounds
        
    
    def traverse_map(self) -> bool:
        travelling = True
        while travelling:
            travelling = self.travel()
            if self.looping:
                return True
        return False
            
    
    def count_footprints(self) -> int:
        return sum(
            x > 0
            for row in self.data
            for x in row
        )
    def find_footprints(self) -> int:
        return tuple(
            (x, y)
            for y, row in enumerate(self.data)
            for x, col in enumerate(row)
            if col > 0
        )
    
def task_1():
    gm = GuardMap(FILENAME)
    gm.traverse_map()
    return gm.count_footprints()

def task_2():
    from tqdm import tqdm
    gm = GuardMap(FILENAME)
    gm.traverse_map()
    possible_obstacles = gm.find_footprints()
    n_loops = 0
    for po in tqdm(possible_obstacles, 
                   desc="Traversing universes", 
                   ascii=' 123456789#'):
        gm = GuardMap(FILENAME, po)
        if gm.is_same_position(po, gm.position):
            continue
        is_loop = gm.traverse_map()
        if is_loop:
            n_loops += 1
    return n_loops



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
    
# %%
