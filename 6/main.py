#%%
from numpy import prod

# %% 1
print(prod([sum((race[0]-t)*t > race[1] for t in range(race[0])) for race in zip(*[[int(cell) for cell in line.strip().split(' ')[1:] if cell] for line in open("input.txt", 'r')])]))

# %% 2
print(prod([sum((race[0]-t)*t > race[1] for t in range(race[0])) for race in zip(*[[int(''.join(line.strip().split(' ')[1:]))] for line in open("input.txt", 'r')])]))

