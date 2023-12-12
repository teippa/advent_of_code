# %%


with open('input.txt', 'r') as F:
    instructions = F.readline().strip()
    F.readline()
    graph = {}
    for line in F.readlines():
        
        node, LR = line.strip().split(' = ')
        graph[node] = dict(zip('LR', LR[1:-1].split(', ')))

shortcuts = {}
for node in graph.keys():
    currently_at = node
    for pos, n in enumerate(instructions):
        currently_at = graph[currently_at][n]

        if currently_at == 'ZZZ':
            break
            
    shortcuts[node] = (
        currently_at, 
        pos+1,
    )

# %% 1
currently_at = 'AAA'
path_length = 0
while currently_at != 'ZZZ':
    currently_at, distance_travelled = shortcuts[currently_at]
    path_length += distance_travelled

print(path_length)


# %% 2
import numpy as np

currently_at = [node for node in shortcuts.keys() if node.endswith('A')]
path_lengths = np.array([0,0,0,0,0,0])
caulcuating = np.ones(path_lengths.shape).astype(bool)

while caulcuating.sum() != 0:
    for lr in instructions:
        currently_at = [graph[node][lr] for node in currently_at]

        path_lengths[caulcuating] += 1

        caulcuating[np.array([node.endswith('Z') for node in currently_at])] = False

print(path_lengths)

print(np.lcm.reduce(path_lengths.astype(np.int64)))




# %% Visualize part 2

import networkx as nx
import matplotlib.pyplot as plt
from pyvis.network import Network

def get_color(name):
    if name.endswith('A'):
        return 'cyan'
    elif name.endswith('Z'):
        return 'orange'
    return 'green'

G = nx.DiGraph()

G.add_nodes_from([
    (n, {
        'size': 30,
        'color': get_color(n),
    })
    for n in graph.keys()])
G.add_edges_from([(k, ep) for k, v in graph.items() for ep in v.values()])


net = Network('80vh', '100%', bgcolor="#222222", font_color="white", select_menu=True)
net.from_nx(G)
net.show_buttons(filter_=['physics'])
net.save_graph('nx.html')

