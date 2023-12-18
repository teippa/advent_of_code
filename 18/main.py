# %%
import numpy as np

path = ''
with open("input_example.txt", 'r') as F:
    
    for line in F.readlines():
        direction, n, collor = line.split(' ')
        path += direction * int(n)

#%%
dirs = dict(zip("UDRL", [(0, 1), (0, -1), (1, 1), (1, -1)]))

coords = np.zeros((len(path),2), int)

pos = [0,0]
for i, d in enumerate(path):
    
    coords[i,:] = pos
    x = dirs[d]
    pos[x[0]] += x[1]
    
coords -= coords.min(axis=0)

im = np.zeros(coords.max(axis=0).astype(int) + 1, np.uint8)
for coord in coords:
    # print(coord)
    im[coord[0], coord[1]] = 1
    
    
    
import matplotlib.pyplot as plt

plt.imshow(im)

#%%
import cv2

cnts, hiers = cv2.findContours(im, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

len(cnts)

cv2.contourArea(coords.reshape((-1,1,2))) + len(path)
# %%
np.prod(im.shape)