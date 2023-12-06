#%%
from numpy import prod

# %% 1
with open('input.txt') as file:
    print(prod([sum((race[0]-t)*t > race[1] for t in range(race[0])) for race in zip(*[[int(cell) for cell in line.strip().split(' ')[1:] if cell] for line in file.readlines()])]))

# %% 2
with open('input.txt') as file:
    print(prod([sum((race[0]-t)*t > race[1] for t in range(race[0])) for race in zip(*[[int(''.join(line.strip().split(' ')[1:]))] for line in file.readlines()])]))

