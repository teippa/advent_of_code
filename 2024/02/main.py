#%%
FILENAME = "input.txt"

def load_data(filename: str):
    with open(filename, 'r') as file:
        for line in file.readlines():
            yield [int(i) for i in line.split(' ')]

def is_safe(a: int, b: int, should_increase: bool):
    return ((a<b) == should_increase) and (0 < abs(b-a) < 4)

def report_safety_checker(row: list[int]):
    increasing = row[0] < row[1] 
    for a, b in zip(row, row[1:]):
        safe = is_safe(a, b, should_increase=increasing)
        yield safe
        if not safe:
            return
            


task_1 = sum(
    all(report_safety_checker(row))
    for row in load_data(FILENAME)
)
print("task1:", task_1)



def remove_one_unsafe_and_do_it_all_again(row):
    safe_levels = tuple(report_safety_checker(row))
    n_unsafe_levels = sum(not safe for safe in safe_levels)
    if n_unsafe_levels > 9:
        return False
    if n_unsafe_levels == 0:
        return True

    unsafe_index = safe_levels.index(False)
    try:
        updated = lambda x, i: [*x[:i], *x[i+1:]]
        return any(
            # This could be way more efficient, but my motivation 
            # was depleted long ago because of bad example inputs.
            all(report_safety_checker(updated(row, unsafe_index+i)))
            for i in range(-1,2)
        )
    except IndexError as e:
        # Start or end of list
        print(e)
        return True
    
sum(
    remove_one_unsafe_and_do_it_all_again(row)
    for row in load_data(FILENAME)
)