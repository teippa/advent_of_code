#%%
import numpy as np
import matplotlib.pyplot as plt
import cv2

with open("input.txt", 'r') as F:
    maze_map = np.array([
        list(line.strip())
        for line in F.readlines()
    ])

hills = (maze_map != '#') * (maze_map != '.')

hups = cv2.filter2D(hills.astype(np.uint8), -1, np.ones((3,3)))

fig, ax = plt.subplots(1,1, figsize=(16,16))
ax.set_xticks([])
ax.set_yticks([])
plt.imshow(((maze_map == '.') + 2*hills + 3*(hups>0)).astype(int))

