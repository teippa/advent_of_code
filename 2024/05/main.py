#%%
from collections import defaultdict
FILENAME = 'example_input.txt'
FILENAME = 'input.txt'

from os import path
def load_data(filename: str):
    
    script_path = path.dirname(path.abspath(__file__))
    file_path = path.join(script_path, filename)
    
    rules = defaultdict(set)
    updates = []
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = iter(file.readlines())

        # Loop for reading the rules
        for line in lines:
            if not line.strip():
                break # There is a blank line separating the rules from updates
            a, b = line.strip().split('|')
            rules[int(a)].add(int(b))
            # rules.append(tuple(int(i) for i in line.strip().split('|')))

        # Loop for reading the updates after the rules
        for line in lines:
            updates.append(tuple(int(i) for i in line.strip().split(',')))

    return dict(rules), updates

def get_list_middle_element(l: list):
    return l[ len(l)//2 ]

def order_dict_keys_by_values(d: dict) -> tuple:
    return tuple(
        zip(*sorted(
            d.items(), 
            key=lambda x: x[1]
        ))
    )[0]

def task_1():
    rules, updates = load_data(FILENAME)
    
    good_middle_pages = []
    for pages in updates:
        encountered_pages = set() # Keeps track of encountered pages
        for page in pages:
            encountered_pages.add(page)
            
            # Find pages that are already encountered, but 
            # should be located after the current page
            bad_pages = encountered_pages.intersection(rules.get(page, set()))
            if len(bad_pages):
                break
        else:
            good_middle_pages.append(get_list_middle_element(pages))
    return sum(good_middle_pages)

def task_2():
    # Kind of like task 1, but with extra steps...
    # If we encounter rules that are broken, toss the already encountered
    # pages to the end and continue until everything is (hopefully) in order.
    rules, updates = load_data(FILENAME)
    bad_middle_pages = []
    for update in updates:
        page_processing_queue = list(update)
        page_numbers = { # Gives us the order of pages. This is updated in the while loop
            page: i 
            for i, page in enumerate(update)
        }
        encountered_pages = set() # Remembers which pages are behind the current page
        current_largest_page_number = len(update)
        is_naughty = False # Remembers if we needed to alter the page order
        while len(page_processing_queue):
            page = page_processing_queue.pop(0)
            encountered_pages.add(page)
            
            # Again, find encountered pages that are breaking the rules
            bad_pages = encountered_pages.intersection(rules.get(page, set()))
            for bp in bad_pages:
                # Move the naughty pages back to the queue
                page_processing_queue.append(bp)
                # Update variables that are tracking the state of things
                page_numbers[bp] = current_largest_page_number
                current_largest_page_number += 1
                is_naughty = True
            
            # Bad pages are back in queue, so they are no longer encountered
            encountered_pages.difference_update(bad_pages)
        
        if is_naughty:
            # Only add middle pages if the update was in bad order
            ordered_pages = order_dict_keys_by_values(page_numbers)
            bad_middle_pages.append(get_list_middle_element(ordered_pages))
        
    return sum(bad_middle_pages)
    
    
def timing(fun, n=100):
    import timeit
    exec_time = timeit.timeit(fun, number=n)
    print(f"{fun.__name__} average exec time: {1000*exec_time/n:.4f} ms")    


if __name__ == "__main__":
    
    print(f'task_1: {task_1()}') # 7365
    
    print(f'task_2: {task_2()}') # 5770
    
    timing(task_1) #  6.1358 ms
    timing(task_2) # 19.5241 ms
    