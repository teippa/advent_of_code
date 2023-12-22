#%%
import numpy as np
import matplotlib.pyplot as plt
# from collections import namedtuple

class Brick:
    def __init__(self, brick_start, brick_end):
        self.brick_start = self._parse_coords(brick_start)
        self.brick_end = self._parse_coords(brick_end)

    def _parse_coords(self, coords):
        return np.array([coord for coord in coords.split(',')], dtype=np.int32)
        

    @property
    def brick_coords(self):
        alignment = self.brick_end != self.brick_start
        length = (self.brick_end - self.brick_start).sum() +1
        brick = np.tile(self.brick_start, (length, 1))
        brick.T[alignment, :] += np.arange(length).T
        return brick
    
    def set_height(self, n):
        adjustment = self.brick_start[2] - n
        self.brick_start[2] -= adjustment
        self.brick_end[2] -= adjustment
        return self.brick_end[2]

bricks = []
maximums = np.zeros((1,3), np.uint32)
with open("input.txt", 'r') as file:
    for line in file.readlines():
        b = Brick(*line.strip().split('~'))
        bricks.append(b)
        
        maximums = np.max(np.vstack([maximums, b.brick_coords]), axis=0)
maximums = maximums.astype(int)


torni = np.zeros(maximums+1)
uppis = np.zeros(maximums[[0,1]]+1)
for i, brick in enumerate(sorted(bricks, key=lambda x: x.brick_start[2])):
    coords = brick.brick_coords[:,[0,1]]
    toppis = uppis[coords[:,0], coords[:,1]]
    newppis = np.max(toppis) +1
    newppis = brick.set_height(newppis)
    uppis[coords[:,0], coords[:,1]] = newppis
    for block in brick.brick_coords:
        torni[block[0], block[1], block[2]] = i+1


maximums[2] = max(b.brick_end[2] for b in bricks)+1

#%
def build_image(bricks, dims, maximums):
    im = np.zeros(maximums[dims]+1)
    for i, brick in enumerate(bricks):
        coords = brick.brick_coords[:,dims]
        im[coords[:,0], coords[:,1]]=(i+1)+1000
    return np.rot90(im)



fig, axs = plt.subplots(1,3, figsize=(4,8))
axs[0].imshow(build_image(bricks, [0, 2], maximums))
axs[1].imshow(build_image(bricks, [1, 2], maximums))
# axs[2].imshow(np.rot90(torni.sum(axis=0)>0) )
plt.show()


# <-- Tässä on se kohta kun meni moti

#%%
import networkx as nx
from pyvis.network import Network

# Suunnattu graafi mikä näyttää onko alla ja päällä palikoita jotka ottaa tukea jne
G = nx.DiGraph()

for i in range(maximums[2]-1):
    a = torni[:,:,i].astype(int)
    b = torni[:,:,i+1].astype(int)
    support = (a != b) * (a*b)>0
    for pair in zip(a[support], b[support]):
        a,b = int(pair[0]), int(pair[1])
        G.add_edge(a,b)
G.add_nodes_from(range(1,max(G.nodes)))

can_be_shitted = 0
for n in G.nodes:
    # Jos yllä olevelle palikalla on yli 1 tukipalikka, voidaan tuhota
    tops_supported = all(G.in_degree(up_brick)>1 for _, up_brick in G.out_edges(n))

    # Jos on ylin palikka, voidaan tuhota
    topmost = G.out_degree(n) == 0

    if tops_supported or topmost:
        can_be_shitted += 1

print(can_be_shitted)


#%%
# net = Network()

net = Network(height="75vh", width="100%", bgcolor="#222222", font_color="white")
net.from_nx(G)
net.toggle_physics(True)
net.show_buttons(filter_=['physics'])
net.save_graph('mygraph.html')


# %% Task 2

def chain_reaction(G, n, borke):
    weak_toppers = get_weak_toppers(G, n, borke)
    
    # Merkkaa yllä olevat weak topperit rikkinäisiksi
    borke.update(weak_toppers)
    for topper in weak_toppers:
        # Ketjureaktio jatkuu päällä olevien päälle
        borke = chain_reaction(G, topper, borke)
    
    return borke

def get_weak_toppers(G, n, borke):
    # Topperit on niitä päällä olevia mitkä saattaa tippua ku poistaa palikan
    # Weak topperit on niitä mitkä tippuu
    toppers = [x for _,x in G.out_edges(n)]
    
    weak_toppers = set()
    for topper in toppers:
        topper_supports = {x for x, _ in G.in_edges(topper)}
        is_weak = len(topper_supports - borke) == 0
        if is_weak:
            # If all supports borke
            weak_toppers.add(topper)
    return weak_toppers

chain_reactions = 0
for node in sorted(G.nodes):
    chain_reactions += len(chain_reaction(G, node, {node,}))
    chain_reactions -= 1 # Ekaa ei lasketa

print(chain_reactions)

# %%
