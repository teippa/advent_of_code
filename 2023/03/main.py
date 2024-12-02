#%%
import numpy as np
import cv2
import matplotlib.pyplot as plt

import re

#%%

task_2 = True

def plotFun(im, plot_window=None):
    fig, ax = plt.subplots(figsize=(16,16))
    if plot_window:
        plt.imshow(im[plot_window[0]:plot_window[1],plot_window[0]:plot_window[1]])
    else:
        plt.imshow(im)
    plt.show()

with open('input.txt', 'r') as F:
    schematic = F.read().replace('\n', '.\n').strip()

    numbers = np.array([[char if char.isnumeric() else '.' for char in line] for line in schematic.split('\n')], )

    symbols = np.array([[0 if char in '0123456789.' else 1 for char in line] for line in schematic.split('\n')], np.uint8)
    gears = np.array([[1 if char=='*' else 0 for char in line] for line in schematic.split('\n')], np.uint8)



# %%

# Etsi numerot symbolien vierestä
mask = (cv2.filter2D(symbols, ddepth=-1, kernel=np.ones((3,3))) > 0) * (numbers != '.')
found = 0
while True:
    # Region growing settii löydettyjen lukujen vasemmalle ja oikealle
    mask = (cv2.filter2D(mask.astype(np.uint8), ddepth=-1, kernel=np.ones((1,3))) > 0) * (numbers != '.')

    if mask.sum() == found:
        break
    found = mask.sum()

numbers[mask == False] = '.'

plotFun(mask+symbols*2)

# Etsi regexillä luvut moottorista
print(sum(int(num) for num in re.findall(r"\d+", ''.join(numbers.flatten())))) # 514969

# %%
from math import prod

gear_numbers = []
gear_num_mask = np.zeros(numbers.shape)
for i,j in np.argwhere(gears):
        
    neighborhood = numbers[i-1:i+2, j-3:j+5].copy()
    
    # Region growing settii gearien ympärille
    mask = np.zeros((3,8))
    mask[1,3] = 1
    for _ in range(3):
        mask = cv2.filter2D(mask, ddepth=-1, kernel=np.ones((3,3))) * (neighborhood != '.')
    neighborhood[mask == 0] = '.'
    
    # Etsi regexillä luvut gearin läheisyydestä
    gear_numbers.append([int(num) for num in re.findall(r"\d+", ''.join(neighborhood.flatten()))])

    if len(gear_numbers[-1]) == 2:
        gear_num_mask[i-1:i+2, j-3:j+5][mask > 0] = 1


plotFun(2*gears+gear_num_mask)
    
print(sum(prod(r) for r in gear_numbers if len(r) == 2))


