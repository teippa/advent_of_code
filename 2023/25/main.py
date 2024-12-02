#%%
import numpy as np 
import networkx as nx 
from pyvis.network import Network

G = nx.Graph()

with open('input.txt', 'r') as F:
    for line in F.readlines():
        node, destinations = line.strip().split(': ')
        G.add_node(node, label=node)
        for dest in destinations.split(' '):
            G.add_node(dest, label=dest)
            G.add_edge(node, dest, label=f"{node}-{dest}")


net = Network(height="75vh", width="100%", bgcolor="#222222", font_color="white")
net.from_nx(G)
net.toggle_physics(True)
net.show_buttons(filter_=['physics'])
net.save_graph('mygraph.html')

# KUVASTA NÄHDÄÄN
# xnn-txf
# jjn-nhg
# tmc-lms

# G.remove_edge('xnn', 'txf')
# G.remove_edge('jjn', 'nhg')
# G.remove_edge('tmc', 'lms')

groups = [len(component) for component in nx.connected_components(G)]
print(groups[0] * groups[1])