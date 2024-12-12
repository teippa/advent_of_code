# https://adventofcode.com/2024/day/12
#%% ----------- SETUP -------------------------
from collections import defaultdict
import os
from pprint import pprint
from sys import path as SYSPATH

script_path = os.path.dirname(os.path.abspath(__file__))

SYSPATH.append(os.path.join(script_path, '..'))
from utils import load_data, execute_function

#% --------- THE IMPORTANT STUFF -------------

FILENAME = 'example_input.txt'
FILENAME = 'input.txt'

def new_region():
    return {
        'area': 0,
        'perimeter': 0
    }

class PotteryMap:
    directions = ((0, -1), (1, 0), (0, 1), (-1, 0)) #URDL
    def __init__(self):
        file_path = os.path.join(script_path, FILENAME)
        self.data = load_data(file_path, matrix=True)
        self.correctly_name_regions()
    
    def correctly_name_regions(self):
        reg_i = 1
        for position, pot in self.iterate_pots():
            if isinstance(pot, str):
                self.infect_neighboring_pots(position, search=pot, rename=reg_i)
                reg_i += 1
                
                
    def infect_neighboring_pots(self, position, search: str, rename: int):
        x, y = position
        self[x,y] = rename
        for search_position in self.positions_around(position):
            pot = self.try_get(*search_position)
            if isinstance(pot, str) and pot == search:
                self.infect_neighboring_pots(search_position, search, rename)
                    
            

    def __repr__(self) -> str:
        return '\n'.join((
            ''.join(f"\t{x}" for x in row)
            for row in self.data
        ))
        
    def __getitem__(self, position: tuple[int,int]) -> int:
        x, y = position
        if x<0 or y<0:
            raise IndexError
        return self.data[y][x]
    def __setitem__(self, position: tuple[int,int], value: int) -> bool:
        x, y = position
        if x<0 or y<0:
            raise IndexError
        self.data[y][x] = value
    
    def try_get(self, x: int, y: int, default: int|None = None) -> int:
        try:
            return self[x, y]
        except IndexError:
            return default
    
    def iterate_pots(self):
        for y, row in enumerate(self.data):
            for x, pot in enumerate(row):
                yield (x, y), pot
        
    # def try_set(self, x: int, y: int, value) -> bool:
    #     try:
    #         self[x, y] = value
    #         return True
    #     except IndexError:
    #         return False
    
    def positions_around(self, position: tuple[int,int]):
        for direction in self.directions:
            yield (
                position[0] + direction[0],
                position[1] + direction[1],
            )
    
    def pots_around(self, position: tuple[int,int]):
        for position_around in self.positions_around(position):
            yield self.try_get(*position_around)
        

def task_1():
    pm = PotteryMap()
    regions = defaultdict(new_region)
    # print(pm)
    
    for position, pot in pm.iterate_pots():
        regions[pot]['area'] += 1
        
        for pot_around in pm.pots_around(position):
            if pot_around != pot:
                regions[pot]['perimeter'] += 1
    
    return sum(
        region['area'] * region['perimeter']
        for region in regions.values()
    )

def task_2():
    # pm = PotteryMap()
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
# 	Result: 1374934
# 	Execution time: 739.6958 ms.