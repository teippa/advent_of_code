#%%
from math import floor
import networkx as nx
import matplotlib.pyplot as plt

# %% 1
def task_1():
    points_total = sum(floor(2**(sum(num in card[1] for num in card[0])-1)) for card in [[[int(n) for n in nums.split(' ') if n] for nums in line.strip().split(':')[1].split('|')] for line in open("input.txt", 'r')])

    print(f"{points_total = }")

task_1()


# %% 2
def task_2():
    # Count winnings
    card_wins = [sum(num in card[1] for num in card[0]) for card in [[[int(n) for n in nums.split(' ') if n] for nums in line.strip().split(':')[1].split('|')] for line in open("input.txt", 'r')]]

    # Generate a directed graph of cards
    # Each card can forward to 0-N other cards, which can be kept track of
    G = nx.DiGraph()
    G.add_nodes_from(range(len(card_wins)), times_visited = 1)
    G.add_edges_from([(i, j+1) for i, n_wins in enumerate(card_wins) for j in range(i, i+n_wins)])

    # Pics or it didn't happen
    nx.draw(
        G.subgraph(range(15)), 
        with_labels=True,
        pos=nx.spiral_layout(G), 
    )
    plt.show()


    # Cumulatively increase the times_visited value as we go through the cards in order.
    # There are no loopbacks, so this is simple to calculate
    for node, out_neighbor in G.out_edges:
        G.nodes[out_neighbor]['times_visited'] += G.nodes[node]['times_visited']

    card_total = sum(nx.get_node_attributes(G, "times_visited").values())

    print(f"{card_total = }")

task_2()


# %%
