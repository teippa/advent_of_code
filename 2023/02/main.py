#%%
import numpy as np
from math import prod

# %%

sum([(i+1)*all(int(n) <= {'red': 12, 'green': 13, 'blue': 14,}[color] for n, color in sorted(np.array(line.strip().replace(';','').replace(',','').split(' '))[2:].reshape((-1,2), order='A'), key=lambda x: int(x[0]))) for i, line in enumerate(open('input.txt', 'r').readlines())])


# %%

sum([prod({color:int(n) for n, color in sorted(np.array(line.strip().replace(';','').replace(',','').split(' '))[2:].reshape((-1,2), order='A'), key=lambda x: int(x[0]), reverse=False)}.values()) for i, line in enumerate(open('input.txt', 'r').readlines())])

