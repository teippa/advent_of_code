#%%
import numpy as np
import matplotlib.pyplot as plt
import cv2
from scipy.optimize import root

min_range = 200_000_000_000_000
max_range = 400_000_000_000_000
# min_range = 7
# max_range = 27

class Hail:
    def __init__(self, line):
        coords = [
            int(n) 
            for nums in line.strip().split('@ ') 
            for n in [*nums.split(', ')]
        ]
        self.pos = np.array(coords[:3], dtype=np.float64)# - [min_range, min_range, 0]
        self.vel = np.array(coords[3:], dtype=np.float64)
    
    def f_arr(self, t_arr):
        return np.array([
            self.f(t)
            for t in t_arr
        ])

    def f(self, t):
        return self.pos + self.vel*t
    
    
    def y(self, x):
        t = (x-self.pos[0])/self.vel[0]
        # t = (t>0) * t
        y = self.pos[1] + self.vel[1]*t
        return y
    
    def x(self, y):
        t = (y-self.pos[1])/self.vel[1]
        # t = (t>0) * t
        x = self.pos[0] + self.vel[0]*t
        return x
    
    
    
    


hails = []
with open("input.txt", 'r') as F:
    for line in F.readlines():
        hails.append(Hail(line))

t = np.array([0,min_range])
fig, ax = plt.subplots(1,1, figsize=(16,16))
for hail in hails:
    p = hail.f_arr(t)
    ax.plot(p[:,0], p[:,1], 'k')
ax.set_xlim([min_range, max_range])
ax.set_ylim([min_range, max_range])


crosses = 0
for i, hail1 in enumerate(hails):
    for hail2 in hails[i+1:]:

        z_x = root(lambda x: hail1.y(x)-hail2.y(x), min_range).x
        z_y = root(lambda y: hail1.x(y)-hail2.x(y), min_range).x

        if min_range < z_x < max_range and min_range < z_y < max_range:
            t_hail1 = min((z_x-hail1.pos[0])/hail1.vel[0], (z_y-hail1.pos[1])/hail1.vel[1])
            t_hail2 = min((z_x-hail2.pos[0])/hail2.vel[0], (z_y-hail2.pos[1])/hail2.vel[1])

            if t_hail1 > 0 and t_hail2 > 0:
                ax.plot(z_x, z_y, 'or')
                crosses += 1


print(crosses)



# %%
