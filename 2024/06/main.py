#%% ----------- SETUP -------------------------
import os
from sys import path as SYSPATH

script_path = os.path.dirname(os.path.abspath(__file__))

SYSPATH.append(os.path.join(script_path, '../..'))
from utils import load_data, execute_function

#% --------- THE IMPORTANT STUFF -------------
FILENAME = 'example_input.txt'
FILENAME = 'input.txt'

class GuardMap:
    directions = ((0, -1), (1, 0), (0, 1), (-1, 0)) #URDL
    rotate_history: set[tuple[int, int, int]] = None # set definition must be in __init__ ('mutable default argument pitfall')
    looping = False
    obstacle_memory_thing = None
    start_position = None
    start_direction = None
    def __init__(self, filename, custom_obstacle_position: tuple[int,int]|None = None):
        self.data = self._load_data(filename)
        self.start_position = self._find_starting_position()
        self.start_direction = 0
        self.reset(custom_obstacle_position)
        
    def reset(self, obstacle_position = None):
        # Set to default values and add a new obstacle, if defined
        self.looping = False
        self.position = tuple(self.start_position)
        self._direction_index = self.start_direction
        self.rotate_history = set()
        
        if (self.obstacle_memory_thing is not None):
            # Remove previous obstacle
            x, y, value = self.obstacle_memory_thing
            self[x, y] = value
        
        # Set obstacle somewhere, if defined
        if obstacle_position and not self.is_same_position(self.position, obstacle_position):
            x_o, y_o = obstacle_position
            self.obstacle_memory_thing = (
                x_o,
                y_o,
                self[x_o, y_o]
            )
            self[x_o, y_o] = 0
        else:
            self.obstacle_memory_thing = None
    
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
        if not self._is_in_bounds(x, y):
            raise IndexError
        return self.data[y][x]
    def __setitem__(self, position: tuple[int,int], value: int) -> bool:
        x, y = position
        if not self._is_in_bounds(x, y):
            raise IndexError
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
        return self.try_get(x, y) == 0
    
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
        gm.reset(po)
        if gm.is_same_position(po, gm.start_position):
            continue
        is_loop = gm.traverse_map()
        if is_loop:
            n_loops += 1
    return n_loops

def task_2_rautalanka():
    # Väännetään nyt rautalangasta tämä logiikka ilman hienosteluja
    # Siltikin vastaus on väärä: 1865
    # Latasin myös input datan uudelleen. Ei muutosta
    from itertools import product
    from tqdm import tqdm
    def load_grid(filename: str) -> tuple[tuple[int]]:
        file_path = os.path.join(script_path, filename)
        def str2int(s):
            if s == '#': return 0 # Obstacles are 0
            elif s == '.': return 1 # Empty space is 1
            elif s == '^': return 2 # Starting position is 2
            else: raise Exception('Invalid character in map.')
        return load_data(
            file_path, 
            matrix=True,
            dtype=str2int
        )
    def find_starting_position(grid):
        start_pos_value = 2
        for y, row in enumerate(grid):
            if start_pos_value in row:
                return (row.index(start_pos_value), y)
        raise ValueError("Position not found!")
    
    # gm = GuardMap(FILENAME)
    grid = load_grid(FILENAME)
    size_x, size_y = len(grid[0]), len(grid)
    loop_counter = 0
    directions = ((0, -1), (1, 0), (0, 1), (-1, 0))
    
    def turn_90deg(direction):
        return (direction+1) % 4
        
    def next_step(px, py, direction):
        dx, dy = directions[direction]
        px_new = px+dx
        py_new = py+dy
        return (px_new, py_new)
    
    def pd(p, d):
        return (*p, d)
    
    def get_from_grid(grid, x, y):
        ###################################
        ####### Tämä testi puuttui, #######
        ####### jolloin neg. arvot  #######
        ####### olivat valideja     #######
        ####### koordinaatteja      ####### 
        ###################################
        if x<0 or y<0: return None    #####
        ###################################
        try:
            return grid[y][x]
        except IndexError:
            return None

    # Starting state, same on every loop
    p0 = find_starting_position(grid) # Position 
    d0 = 0 # Direction
    for obstacle_x, obstacle_y in tqdm(product(range(size_x), range(size_y)), total=size_x*size_y, ascii=' #', desc="Placing obstacles"):
        if obstacle_x == p0[0] and obstacle_y == p0[1]:
            # Obstacle can not be on top on guard start position
            continue

        grid = load_grid(FILENAME)
        
        # set obstacle
        grid[obstacle_y][obstacle_x] = 0
        
        action_history = set()
        
        p, d = p0, d0
        while pd(p, d) not in action_history:
            # Add current position and direction to history
            action_history.add(pd(p, d))
            
            try:
                # Find the next step to take
                p_next = next_step(*p, d)
                p_next_value = get_from_grid(grid, *p_next)
                if p_next_value is None:
                    break
                elif p_next_value == 0:
                    # Obstacle found
                    d = turn_90deg(d)
                    p_next = next_step(*p, d)
                    p_next_value = get_from_grid(grid, *p_next)
                    if p_next_value is None:
                        break
                    elif get_from_grid(grid, *p_next) == 0:
                        # Another obstacle found on the right
                        d = turn_90deg(d)
                        p_next = next_step(*p, d)
                        p_next_value = get_from_grid(grid, *p_next)
                        if p_next_value is None:
                            break
                        elif get_from_grid(grid, *p_next) == 0:
                            raise Exception("WTF, I think I have gone through some obstacle... Unless this is the starting position os something...")
            except IndexError:
                # We have gone outside the grid probably, I think
                break
            # Turnings should be done and it should be safe to update position
            p = p_next
            if pd(p, d) in action_history:
                # We should be in a loop
                loop_counter += 1
                break

    return loop_counter
        


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
    
    # execute_function(
    #     task_2_rautalanka,
    #     args = {},
    #     do_timing = do_timing
    # )

# Function: task_1
# 	Result: 4711
# 	Execution time: 126.6394 ms.
# Function: task_2
# 	Result: 1562
# 	Execution time: 151.0967 s.