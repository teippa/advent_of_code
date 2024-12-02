# %%
import pandas as pd
import numpy as np

# %% 1

sum(np.sum([10, 1]*np.array([int(char) for char in row[0] if char.isnumeric()])[[0,-1]]) for row in pd.read_csv('input.txt', delim_whitespace=True, header=None).values)


# %% 2

sum(np.sum([10, 1]*np.array([int(char) for char in row[0].lower().replace('one','one1one').replace('two', 'two2two').replace('three', 'three3three').replace('four', 'four4four').replace('five', 'five5five').replace('six', 'six6six').replace('seven', 'seven7seven').replace('eight', 'eight8eight').replace('nine', 'nine9nine') if char.isnumeric()])[[0,-1]]) for row in pd.read_csv('input.txt', delim_whitespace=True, header=None).values)

