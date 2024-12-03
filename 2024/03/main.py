#%%

from re import finditer
from operator import mul
from itertools import starmap

# FILENAME = 'example_input.txt
FILENAME = 'input.txt'


def load_data(filename: str, header: int = None):
    with open(filename, 'r') as file:
        return file.read()
data = load_data(FILENAME)


def mult_finder(data):
    for match in finditer(r'mul\((\d\d?\d?),(\d\d?\d?)\)', data):
        yield int(match[1]), int(match[2])

# def do_finder(data):
#     for match in finditer(r'do\(\)', data):
#         yield match.start()

# def dont_finder(data):
#     for match in finditer(r'don\'t\(\)', data):
#         yield match.start()
    
    
def one_finder_to_rule_them_all(data):
    yield_switch = True
    for match in finditer(r'(?P<do>do\(\))|(?P<dont>don\'t\(\))|mul\((\d\d?\d?),(\d\d?\d?)\)', data):
        if match.group('do'):
            yield_switch = True
        elif match.group('dont'):
            yield_switch = False
        elif yield_switch:
            yield int(match[3]), int(match[4])
    
    
    
if __name__ == "__main__":
    
    task_1 = sum(starmap(mul, mult_finder(data)))
    print(f"{task_1 = }")
        
    task_2 = sum(starmap(mul, one_finder_to_rule_them_all(data)))
    print(f"{task_2 = }")

