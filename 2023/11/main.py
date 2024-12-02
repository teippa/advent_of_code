#%%
import numpy as np

with open("input.txt", 'r') as F:
    galaxy = np.array([
        [char == '#' for char in line.strip()]
        for line in F.readlines()
    ])
    
#%%
def is_between(n, x):
    return sum((n < x[0], n < x[1])) == 1

def main(part_2 = False):
    x_empties = np.argwhere(galaxy.sum(axis=0) == 0).flatten().tolist()
    y_empties = np.argwhere(galaxy.sum(axis=1) == 0).flatten().tolist()

    star_positions = np.argwhere(galaxy == True)

    distances = np.zeros((len(star_positions), len(star_positions)), np.uint64)
    for i, pos_1 in enumerate(star_positions):
        for j, pos_2 in enumerate(star_positions):
            x_expansions = sum(is_between(spot, [pos_1[1], pos_2[1]]) for spot in x_empties)
            y_expansions = sum(is_between(spot, [pos_1[0], pos_2[0]]) for spot in y_empties)
            
            if part_2:
                x_expansions *= (10**6-1)
                y_expansions *= (10**6-1)
            
            if j > i:
                distances[i,j] = np.abs(pos_2-pos_1).sum() + x_expansions + y_expansions

    return distances.sum() # 374

print(main())
print(main(part_2 = True))

# %%
