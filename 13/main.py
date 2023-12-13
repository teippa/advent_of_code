#%%
import numpy as np

with open("input.txt", 'r') as F:
    patterns = [
        np.array([
            list(line)
            for line in structure.split('\n')
        ])
        for structure in F.read().strip().split("\n\n")
    ]

def mirror_detector(arr):
    zero_positions = np.argwhere(arr < 2).flatten()
    results = []
    for zp in zero_positions:
        is_mirror = True
        smudge_found = zp == 1
        for i in range(1,arr.size):
            a, b = zp-i, zp+i
            if a < 0 or b>arr.size-1:
                break
            # print(arr[a], arr[b])
            # if not smudge_found and abs(arr[a] - arr[b]) == 1:
            #     smudge_found = True
            # el
            if arr[a] != arr[b]:
                is_mirror = False
                break
            
        if is_mirror:
            # if result != 0:
            #     # Multiple horizontal / vertical mirrors found
            #     print("Something's fucky...")
            results.append([(zp == 1), zp+1])
    
    if results:
        return max(results)
    else:
        return (False, 0)

total = 0
for p in patterns:
    horizontal_differences = np.diff(p=='#', axis=0).sum(axis=1)
    vertical_differences = np.diff(p=='#', axis=1).sum(axis=0)
    
    h = mirror_detector(horizontal_differences)
    v = mirror_detector(vertical_differences)
    
    if h[1] > 0 and v[1] > 0:
        h[1] *= h[0]
        v[1] *= v[0]
        
    total += 100*h[1] + v[1]
    
total

# %%
