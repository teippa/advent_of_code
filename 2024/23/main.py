# https://adventofcode.com/2024/day/23
#%% ----------- SETUP -------------------------
from __future__ import annotations
import os
from sys import path as SYSPATH
from typing import Generator
import networkx as nx

from tqdm import tqdm

script_path = os.path.dirname(os.path.abspath(__file__))

SYSPATH.append(os.path.join(script_path, '../..'))
from utils import load_data, execute_function

#% --------- THE IMPORTANT STUFF -------------

FILENAME = 'example_input.txt'
FILENAME = 'input.txt'
file_path = os.path.join(script_path, FILENAME)

class Node:
    def __init__(self, label):
        self.label: str = label.strip()
        self.nodes_in: set[Node] = set()
        self.nodes_out: set[Node] = set()

    def __repr__(self):
        return f"Node[{self.label}]"

    @property
    def degree(self):
        return len(self.nodes_in) + len(self.nodes_out)
    
    @property 
    def neighbors(self):
        return set.union(self.nodes_in, self.nodes_out)

class Graph:
    def __init__(self):
        self.nodes: dict[str, Node] = dict()
    
    def __iter__(self) -> Generator[Node, None, None]:
        for node in self.nodes.values():
            yield node
    
    def new_node(self, label: str) -> Node:
        node = Node(label=label)
        self.nodes[label] = node
        return node


    def get_node(self, label: str) -> Node:
        node = self.nodes.get(label, None)
        if node is None:
            node = self.new_node(label)
        return node

    def add_link(self, label_from: str, label_to: str):
        node_from = self.get_node(label_from)
        node_to = self.get_node(label_to)
        node_to.nodes_in.add(node_from)
        node_from.nodes_out.add(node_to)

    def has_connection(self, label_1: str, label_2: str) -> bool:
        node_1 = self.get_node(label_1)
        node_2 = self.get_node(label_2)
        return node_1 in node_2.neighbors

    def find_cycles(self, target: Node, depth: int, node: Node):
        cycles = []
        if depth == 0:
            if target in node.neighbors:
                return ((target,),)
            else:
                return []
        print(depth, node, node.neighbors)
        for neighbor in node.neighbors.difference((target,)):
            cycles.extend(
                (node, *c)
                for c in self.find_cycles(target, depth-1, neighbor)
            )

        return cycles

        ## THIS SHOULD RETURN LIST OF NODES, NOT BOOLEAN

    def cycles_3(self):
        for node in self.nodes.values():
            print('\t', node)
            print('\tNEIGH:', node.neighbors)
            print('Cycles', self.find_cycles(node, 3, node))
            # break

def custon_graph_attempt():
    
    data = load_data(
        file_path, 
        lines=True, 
        dtype=lambda x: [x.strip() for x in x.split('-')]
    )
    # print(data)
    graph = Graph()
    for label_from, label_to in data:
        graph.add_link(label_from, label_to)

    return len(graph.cycles_3())



def task_1():
    data = load_data(
        file_path, 
        lines=True, 
        dtype=lambda x: x.strip().split('-')
    )

    # Create a graph
    G = nx.Graph()
    for v, u in tqdm(data, desc='Adding edges'):
        G.add_edge(v, u)

    cycles = set(
        frozenset(cycle)
        for cycle in tqdm(nx.simple_cycles(G, 3), desc='Finding cycles')
        if (len(cycle) == 3) and any(n.startswith('t') for n in cycle)
    )
    # import matplotlib.pyplot as plt
    # nx.draw(G, with_labels=True, node_color='lightblue', edge_color='gray', node_size=500, font_size=16)
    # plt.show()

    return len(cycles)

def task_2():
    data = load_data(
        file_path, 
        lines=True, 
        dtype=lambda x: x.strip().split('-')
    )
    # Create a graph
    G = nx.Graph()
    for v, u in tqdm(data, desc='Adding edges'):
        G.add_edge(v, u)

    max_degree = max(G.degree())[1]
    print(f"{max_degree = }")

    max_deg_nodes = [
        node
        for node, deg in G.degree()
        if deg == max_degree
    ]

    return ','.join(sorted(max_deg_nodes))



#% -------------------------------------------

if __name__ == "__main__":
    do_timing = False
    # execute_function(
    #     task_1,
    #     args = {},
    #     do_timing = do_timing
    # )
    
    execute_function(
        task_2,
        args = {},
        do_timing = do_timing
    )
    
# %%
