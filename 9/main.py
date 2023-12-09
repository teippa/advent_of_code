# %%
import numpy as np

# %%

def aargh(nums):
    if all(nums == 0):
        return 0
    else:
        x = aargh(np.diff(nums))
        return x+nums[-1]


sum_extrapolated_fw = sum([aargh(np.array([int(num) for num in line.split(' ')])) for line in open("input.txt", 'r').readlines()])

sum_extrapolated_bw = sum([aargh(np.array([int(num) for num in line.split(' ')][::-1])) for line in open("input.txt", 'r').readlines()])

print(f"{sum_extrapolated_fw}\n{sum_extrapolated_bw}")

