# %%
import numpy as np
import cv2
import matplotlib.pyplot as plt
import imageio

task_2 = False

with open('input.txt', 'r') as file:
    potmap = np.array([list(line) for line in file.read().strip().split('\n')])

kernel = np.array([[0,1,0],[1,0,1],[0,1,0]])

# %% Task 1 (& 2)

pots = (potmap != '#')
canvas = (potmap == 'S').astype(np.uint8)

save_image_size = (canvas.shape[0]*4, )*2

X = 19
if task_2:
    S_pos = (np.argwhere(canvas)  + np.array(canvas.shape)*(X//2)).flatten().tolist()
    pots = np.hstack([np.vstack([pots,]*X),]*X)
    canvas = np.zeros(pots.shape)
    canvas[S_pos[0], S_pos[1]] = 1
sums = []

with imageio.get_writer('movie.gif', mode='I', duration=0.5) as writer:
    for i in range(64 + task_2*(X-1)*64):
        
        canvas = ((cv2.filter2D(canvas, -1, kernel) > 0) * pots).astype(np.uint8)
        if not task_2:
            writer.append_data(cv2.resize(
                (canvas*255 + (pots == 0)*150).astype(np.uint8), 
                save_image_size,  
                interpolation = cv2.INTER_AREA
            ))
        sums.append(canvas.sum())
        
plt.imshow(canvas+(pots-1))
plt.show()
print(canvas.sum())

#%% Task 2
from scipy.optimize import curve_fit

x = np.array(sums[0:2000])
inds = np.arange(len(x))


f = lambda x, a,b,c,d: a*x**3 + b*x**2 + c*x + d
a, *_ = curve_fit(f, inds, x)

print(a)
x_1 = (x - f(inds, *a)) 

plt.plot(x_1)
plt.plot(inds)
plt.plot(-inds)
plt.show()

print(f(26501365, *a).astype(np.uint64), "+/-", 26501365)


# %%
