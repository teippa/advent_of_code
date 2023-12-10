#%%

import numpy as np
import matplotlib.pyplot as plt
import cv2

#%%

largefy_dict = {
    'J': np.array([0, 1, 0, 
                   1, 1, 0, 
                   0, 0, 0,]).reshape(3,3),
    'L': np.array([0, 1, 0, 
                   0, 1, 1, 
                   0, 0, 0,]).reshape(3,3),
    '-': np.array([0, 0, 0, 
                   1, 1, 1, 
                   0, 0, 0,]).reshape(3,3),
    '|': np.array([0, 1, 0, 
                   0, 1, 0, 
                   0, 1, 0,]).reshape(3,3),
    '7': np.array([0, 0, 0, 
                   1, 1, 0, 
                   0, 1, 0,]).reshape(3,3),
    'F': np.array([0, 0, 0, 
                   0, 1, 1, 
                   0, 1, 0,]).reshape(3,3),
    'S': np.array([0, 1, 0, 
                   1, 2, 1, 
                   0, 1, 0,]).reshape(3,3),
    '.': np.zeros((3,3)),
}




#%%


with open('input.txt', 'r') as F:
    field = np.array([ list(line.strip()) for line in F.readlines()])


def plots_for_fun(field, save = False):
    fig, ax = plt.subplots(figsize = (16,16))
    ax.imshow(field)
    plt.show()
    if save:
        plt.imsave('fig.png', field)

def create_big_field(field):
    field_size = [3*s for s in field.shape]
    big_field = np.zeros(field_size)
    for i, x in enumerate(range(0,field_size[0],3)):
        for j, y in enumerate(range(0,field_size[1],3)):
            big_field[x:x+3, y:y+3] = largefy_dict[field[i,j]]
    return big_field


def find_path(big_field):

    path = (big_field > 1)
    path_len = 0
    while path_len != path.sum():
        path_len = path.sum()
        path = cv2.filter2D((path>0).astype(np.uint8), ddepth=2, kernel=largefy_dict['S']) * big_field

    return (path>0).astype(np.uint8)

# %%
#### Task 1

big_field = create_big_field(field)
path = find_path(big_field)

plots_for_fun(big_field + path)

path_total_length = (path.sum()-2)/3 # Starting cell has 2 extra dots
print((path_total_length/2).astype(int))

# %% 
#### Task 2

def find_loop_outsides(path):
    outside = np.zeros(path.shape)
    outside[0,0] = 1

    ground = path == 0
    outside_size = 0
    while outside_size != outside.sum():
        outside_size = outside.sum()
        outside = cv2.filter2D(outside.astype(np.uint8), ddepth=-1, kernel=np.ones((3,3))) * ground
    return outside


thick_path = cv2.filter2D(path.astype(np.uint8), ddepth=2, kernel=np.ones((3,3)))>0
outside = find_loop_outsides(path)

insides = (outside == 0) * (thick_path == 0)

plots_for_fun(
    5*insides + 2*path + thick_path, 
    save = False
)

print((insides.sum()/9).astype(int))

# %%