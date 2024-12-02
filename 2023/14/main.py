#%%
import numpy as np
import matplotlib.pyplot as plt


with open("input.txt", 'r') as F:
    slab = np.array([
        [c for c in line]
        for line in F.read().strip().split('\n')
    ])

def roll_up(slab):
    roll_end = np.zeros(slab[0,:].shape, int)
    for i, row in enumerate(slab):
        stones = np.argwhere(row == 'O')
        for stone in stones:
            row[stone], slab[roll_end[stone], stone] = slab[roll_end[stone], stone], row[stone]
            roll_end[stone] += 1
        roll_end[row == '#'] = i+1
    return slab

def roll_cycle(slab):
    for _ in range(4):
        slab = np.rot90(roll_up(slab), -1)
    return slab

def count_weight(slab):
    total = 0
    for i, row in enumerate(np.flipud(slab)):
        total += np.sum(row == 'O')*(i+1)
    return total

# %% Task 1
print(count_weight(roll_up(slab))) # 108840


# %% Task 2

weights = set()
combo = 0
pattern = []
n_cycles = 1_000_000_000 
for i in range(n_cycles):
    slab = roll_cycle(slab.copy())
    weight = count_weight(slab)
    
    # Detect if we are on a cycle and stop early
    if weight in weights:
        if combo:
            pattern.append(weight)
            x = len(pattern)//2
            if len(pattern)%2 == 0 and pattern[0:x] == pattern[x:]:
                # Calculate were we are on the pattern at the end of cycles
                n = n_cycles - (i + x*((n_cycles-i)//x)) - 2
                final_weight = pattern[n]
                break
        else:
            pattern = []
        combo = True
    else:
        combo = False
        
    weights.add(weight)
    
print(final_weight) # 103445


# %%
