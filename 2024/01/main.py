#%%
from collections import Counter
import pandas as pd
import math

data = pd.read_fwf('input.txt', header=None).values.tolist()


#%% 1
def sorter(rows):
    return zip(*(
        sorted(column)
        for column in zip(*rows)
    ))

sum(
    abs(a-b) 
    for a, b in sorter(data)
) #1938424


#%% 2
def counter(rows):
    return (
        Counter(column)
        for column in zip(*rows)
    )

numbers, similarities = counter(data)

sum(
    num*count*similarities.get(num, 0)
    for num, count in numbers.items()
) # 22014209
