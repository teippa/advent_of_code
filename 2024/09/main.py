# https://adventofcode.com/2024/day/9
#%% ----------- SETUP -------------------------
from collections import namedtuple
from math import prod
import os
from sys import path as SYSPATH

script_path = os.path.dirname(os.path.abspath(__file__))

SYSPATH.append(os.path.join(script_path, '..'))
from utils import load_data, execute_function

#%% --------- THE IMPORTANT STUFF -------------

FILENAME = 'example_input.txt'
FILENAME = 'input.txt'
file_path = os.path.join(script_path, FILENAME)



def task_1():
    data = load_data(file_path)
    disc = [
        None if i%2 else i//2
        for i, c in enumerate(data.strip())
        for _ in range(int(c))
    ]
    
    def consume_disc(disc):
        print(disc)
        i_start = 0
        i_end = len(disc)-1
        while i_start <= i_end:
            val_start = disc[i_start]
            i_start += 1
            if val_start is not None:
                # Yield values from the beginning of disc 
                yield val_start
            else:    
                # When empty spaces are encountered,
                # yield a value from the end of disc instead                
                while i_start <= i_end:
                    val_end = disc[i_end]
                    i_end -= 1
                    if val_end is not None:
                        yield val_end
                        break
    hash_sum = sum(map(prod, enumerate(consume_disc(disc))))
    return hash_sum

def task_2():
    section = namedtuple("Section", 'id,len')
    empty_section = lambda size: section(None, size)
    
    def load_sections():
        data = load_data(file_path)
        sections = [] # files and empty spaces
        pos = 0
        for i, c in enumerate(data.strip()):
            if c == '0':
                # No need to add 0-length sections
                continue
            if i%2 == 1:
                sections.append(empty_section(int(c)))
            else:
                sections.append(section(i//2, int(c)))
            pos += int(c)
        return sections
    
    def insert_section(sections, index, sect):
        if sect.len > sections[index].len:
            raise IndexError("Target length is smaller than source.")
        if not (sections[index].id is None):
            raise IndexError("Target is not empty.")
                
        old_empty = sections.pop(index)
        if sect.len < old_empty.len:
            new_empty = empty_section(old_empty.len - sect.len)
            sections.insert(index, new_empty)
        sections.insert(index, sect)
        
    def find_fitting_empty_space(sections, sect):
        for i, section in enumerate(sections):
            if (section.id is None) and sect.len <= section.len:
                return i
        return -1
    
    def compactify_sections(sections):
        compacted_sections = []
        while len(sections):
            # Pop the last section and try to find a place for it
            last_section = sections.pop()
            if (last_section.id is None):
                # if section is empty, add it straigth to the compacted
                compacted_sections.insert(0, last_section)
                continue
            
            # Try to find a place for the section
            target_ind = find_fitting_empty_space(sections, last_section)
            
            if target_ind == -1:
                # Not enough space anywhere
                compacted_sections.insert(0, last_section)
            else:
                # Section can be moved somewhere
                insert_section(sections, target_ind, last_section)
                # The section leaves behind empty space when it is moved
                compacted_sections.insert(0, empty_section(last_section.len))
        return compacted_sections
    
    
    def calculate_hash(sections):
        hash_sum = 0
        i = 0
        for section in sections:
            for _ in range(section.len):
                if (section.id is not None):
                    hash_sum += i*section.id
                i += 1
        return hash_sum
    
    sections = load_sections()
    sections = compactify_sections(sections)
    
    return calculate_hash(sections)



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
