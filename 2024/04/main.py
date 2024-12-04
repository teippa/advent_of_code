#%%
from itertools import product
# FILENAME = 'example_input.txt'
FILENAME = 'input.txt'


class XmasFinder:
    # Directions for task 1
    search_directions = tuple(
        (a, b) 
        for a, b in product((-1,0,1), repeat=2) 
        if not (a == 0 and b == 0)
    )
    # Directions for task 2
    x_directions = tuple(
        (a, b) 
        for a, b in product((-1,1), repeat=2) 
    )
    
    def __init__(self, filename: str):
        self.data = self._load_data(filename)
        self.shape = self._calculateShape()
    
    def __repr__(self) -> str:
        return '\n'.join((
            ''.join(row)
            for row in self.data
        ))
    
    def _load_data(self, filename: str) -> list[list[str]]:
        """ Load the data from file
        """
        with open(filename, 'r') as file:
            return [
                list(line.strip())
                for line in file.readlines()
            ]
        
    def _calculateShape(self) -> tuple[int, int]:
        y = len(self.data)
        x = 0 if y==0 else len(self.data[0])
        return (x, y)
    
    
    
    def _coords_in_bounds(self, x: int, y: int) -> bool:
        """ Checks if the coordinates are within data bounds
        """
        ob_x, ob_y = self.shape
        return (0 <= x < ob_x) and (0 <= y < ob_y)
    
    def _char_at(self, x: int, y: int) -> str:
        """ Retrieves a character from data
        """
        if not self._coords_in_bounds(x, y):
            return None
        return self.data[y][x]
    
    def _move_to_direction(self, position: tuple[int, int], direction: tuple[int, int]) -> tuple[int, int]:
        """ Translates coordinates to specified direction
        """
        return (
            position[0] + direction[0],
            position[1] + direction[1],
        )
        

    def word_search(self, input_word: list[str] | str, current_position: tuple[int, int], direction: tuple[int, int]) -> bool:
        """ Recursive function that consumes the input_word and returns True if every character was found 
            in order, while traversing towards a direction
        """
        finding_char, *sliced_word = input_word
        
        if self._char_at(*current_position) != finding_char:
            return False
        
        if len(sliced_word) == 0:
            return True
        
        next_position = self._move_to_direction(current_position, direction)
        return self.word_search(
            sliced_word,
            next_position,
            direction
        )
    
    def char_finder(self, char: str) -> list[tuple[int, int]]:
        """ Find all coordinates for a character within the data
        """
        indexes = list()
        for y, row in enumerate(self.data):
            for x, s in enumerate(row):
                if s == char:
                    indexes.append((x, y))
        return indexes
    
    
    def do_the_task_1(self) -> int:
        """ Finding 'XMAS words by starting from 'X' and continuing search to all directions 
        """
        word_to_find = "XMAS"
        
        first_char = word_to_find[0]
        first_char_positions = self.char_finder(first_char)
        
        return sum(
            self.word_search(word_to_find, position, direction)
            for position, direction in product(first_char_positions, self.search_directions)
        )
        
    def do_the_task_2(self) -> int:
        """ Finding character patterns that form 'MAS' in X formation around 'A' characters
        """
        good_patterns = set(('MMSS', 'MSMS', 'SSMM', 'SMSM'))
        n = 0
        for a_position in self.char_finder('A'):
            word = ''
            for direction in self.x_directions:
                pos = self._move_to_direction(a_position, direction)
                if not self._coords_in_bounds(*pos):
                    break
                word += self._char_at(*pos)

            if word in good_patterns:
                n += 1
        
        return n
            
        

if __name__ == "__main__":
    xf = XmasFinder(FILENAME)
    
    print(xf.do_the_task_1())
    
    print(xf.do_the_task_2())
    
    # I wrote this line to change a git commit message
    
