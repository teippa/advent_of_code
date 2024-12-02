# %%
import numpy as np
import matplotlib.pyplot as plt
import cv2
import re

with open("input.txt", 'r') as F:
    lines = F.readlines()

# %% Task 1
dirs_1 = dict(zip("RDLU", [
    np.array((1, 0)), 
    np.array((0, -1)), 
    np.array((-1, 0)), 
    np.array((0, 1)), 
]))

def parse_instructions_1(line):
    direction, n, color = line.split(' ')
    return dirs_1[direction] * int(n) 


coords = np.zeros((len(lines),2), np.int64)
pos = [0,0]
for i, line in enumerate(lines):
    coords[i,:] = pos
    pos += parse_instructions_1(line)

coords -= coords.min(axis=0)
im = np.zeros(coords.max(axis=0).astype(int) + 1, np.uint8)
    
cv2.drawContours(im, [np.fliplr(coords),], 0, 1, -1)

fig = plt.imshow(im)
plt.title("Kyttyräselkämuurahainen")
plt.imsave("tärkee.png", fig)
im.sum() # 50465
# %% Task 2

dirs_2 = list(dirs_1.values())

def parse_instructions_2(line):
    _, n, direction, _ = re.split(r'\(#(.+)(\d)\)', line)
    direction = int(direction)
    length = int(n, 16)
    return dirs_2[direction], length

coords = np.zeros((len(lines),2), np.int64)
pos = [0,0]
piiri = 0
for i, line in enumerate(lines):
    coords[i,:] = pos
    direction, length = parse_instructions_2(line)
    pos += direction * length
    piiri += length

x = coords[:,0]
y = coords[:,1]

# Shoelace formula
area=0.5*np.sum(y[:-1]*np.diff(x) - x[:-1]*np.diff(y))
area=np.abs(area)

totin_fix = piiri/2+1 # Thanks Totti <3

print(area + totin_fix)

# %%
