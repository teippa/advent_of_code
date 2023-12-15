#%%
import numpy as np
import matplotlib.pyplot as plt

with open("input.txt", 'r') as F:
    patterns = [
        np.array([
            list(line)
            for line in structure.split('\n')
        ])
        for structure in F.read().strip().split("\n\n")
    ]
    
def mirror_detector(pattern, smudge_detection = False):
    differences = np.diff(pattern=='#', axis=0).sum(axis=1)
    zero_positions = np.argwhere(np.abs(differences) < (1+smudge_detection)).flatten()
    for zp in zero_positions:
        is_valid_mirror = True
        
        # Set smudge immideatedy as detected if detection is turned off
        smudge_detected = not smudge_detection

        for i in range(differences.size//2):
            a, b = zp-i, zp+i+1
            if a < 0 or differences.size < b:
                # Break if out of bounds
                break
            
            # Rows to inspect, should be similar
            rows = np.array([pattern[a,:], pattern[b,:]])

            n_differences = np.diff(rows=='#', axis=0).sum()
            if not smudge_detected and n_differences == 1:
                smudge_detected = True
            elif n_differences > 0:
                is_valid_mirror = False
                break
        
        if is_valid_mirror and smudge_detected:
            return zp+1
    
    return 0

def mirror_value(pattern, smudge_detection=False):
    h = mirror_detector(pattern, smudge_detection)
    v = mirror_detector(pattern.transpose(), smudge_detection)

    return 100*h + v
    

total = sum(mirror_value(pattern) for pattern in patterns)
smudge_total = sum(mirror_value(pattern, smudge_detection=True) for pattern in patterns)

    
print(f"{total = }") # 30518
print(f"{smudge_total = }") # 36735

# %%
