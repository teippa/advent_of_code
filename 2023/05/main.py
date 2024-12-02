# %%
import numpy as np

def is_in_range(num, area):
    return area[1] <= num <= area[1]+area[2]

def find_end_point(num, maps):
    for area in maps:
        if is_in_range(num, area):
            # print(f"{num-area[1] = }")
            # print(f"{area[0] = }")
            # print(f"{area[0] + (num - area[1]) = }")
            return area[0] + (num - area[1])
    return num


with open('input.txt', 'r') as F:
    setit = F.read().strip().split('\n\n')
    seeds = [int(num) for num in setit[0].split(' ')[1:]]

    maps_dict = {
        setti.split(' map:')[0]: [
            [int(num) for num in row.split(' ')]
            for row in setti.split('\n')[1:]
        ]
        for setti in setit[1:]
    }

location_numbers = np.zeros((len(seeds),1))
for i, seed in enumerate(seeds):
    n = seed
    for maps_name, maps in maps_dict.items():
        # print(maps_name)
        n_end = find_end_point(n, maps)
        # print(n, '->', n_end)
        n = n_end
    location_numbers[i] = n

print(location_numbers.min().astype(int))

