
"""
    This is a helper class to retrieve dara from the input.
    It also FIXES the input/map, since the elves can't seem to do anything properly.
"""

class PotteryMap:
    directions = ((0, -1), (1, 0), (0, 1), (-1, 0)) #URDL
    regions = None
    def __init__(self, data):
        self.data = data
        self.regions = set()
        self.correctly_name_regions()

    
    def correctly_name_regions(self):
        # The elves can't be bothered to name their pot regions properly,
        # so I guess I have to do it for them.
        reg_i = 1
        for position, pot in self.iterate_pots():
            if isinstance(pot, str):
                self.infect_neighboring_pots_with_correct_name(position, search=pot, rename=reg_i)
                self.regions.add(reg_i)
                reg_i += 1
                
    def infect_neighboring_pots_with_correct_name(self, position, search: str, rename: int):
        # This recursively spreads the correct region name/index to the entire region
        x, y = position
        self[x,y] = rename
        for search_position in self.positions_around(position):
            pot = self.try_get(*search_position)
            if isinstance(pot, str) and pot == search:
                self.infect_neighboring_pots_with_correct_name(search_position, search, rename)


    def __repr__(self) -> str:
        return '\n'.join((
            ''.join(f"\t{x}" for x in row)
            for row in self.data
        ))
        
    def __getitem__(self, position: tuple[int,int]) -> int:
        x, y = position
        if x<0 or y<0:
            raise IndexError("Only positive coordinates are allowed")
        return self.data[y][x]
    
    def __setitem__(self, position: tuple[int,int], value: int) -> bool:
        x, y = position
        if x<0 or y<0:
            raise IndexError("Only positive coordinates are allowed")
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

    def get_region_positions(self, region_i):
        for position, pot in self.iterate_pots():
            if pot == region_i:
                yield position