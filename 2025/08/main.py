# https://adventofcode.com/2025/day/8

#%% ----------- SETUP -------------------------
from math import prod
import os
import sys

script_path = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_path, '..', '..'))

sys.path.append(project_root)
from utils import load_data, execute_function

#%% --------- THE IMPORTANT STUFF -------------

def split_and_cast(row: str):
    return list(map(int, row.split(',')))

def square_distance(p0, p1):
    return sum((b-a)**2 for a, b in zip(p0, p1))


def join_graphs(graphs):
    new_graphs = []
    for graph in graphs:
        for grph in new_graphs:
            if any(link in grph for link in graph):
                grph.update(graph)
                break
        else:
            new_graphs.append(graph)
    if len(new_graphs) != len(graphs):
        return join_graphs(new_graphs)
    return new_graphs
    
def task_1(input_path: str, n_links: int = 1000):
    data = load_data(input_path, lines=True, dtype=split_and_cast)
    pairs = [] # (i_p0, i_p1, distance)
    
    # Calculate all distances
    for i, p0 in enumerate(data[:-1]):
        for j, p1 in enumerate(data[i+1:], start=i+1):
            distance = square_distance(p0, p1)
            pairs.append((set((i, j)), distance))
                
    short_links= sorted(pairs, key=lambda x: x[-1])
    
    additions = 0
    graphs = []
    for link, distance in short_links:
        for graph in graphs:
            checks = [node in graph for node in link]
            if all(checks):
                continue
            elif any(checks):
                graph.update(link)
                additions += 1
                break
        else:
            graphs.append(link)
            additions += 1
        if additions >= n_links:
            break
    
    
    joined_graphs = join_graphs(graphs)
    
    return prod(sorted(map(len, joined_graphs), reverse=True)[:3])
    

def task_2(input_path: str):
    data = load_data(input_path, lines=True, dtype=split_and_cast)
    pairs = [] # (i_p0, i_p1, distance)
    
    # Calculate all distances
    for i, p0 in enumerate(data[:-1]):
        for j, p1 in enumerate(data[i+1:], start=i+1):
            distance = square_distance(p0, p1)
            pairs.append((set((i, j)), distance))
                
    short_links= sorted(pairs, key=lambda x: x[-1])
    
    additions = 0
    graphs = []
    for link, distance in short_links:
        for graph in graphs:
            checks = [node in graph for node in link]
            if all(checks):
                continue
            elif any(checks):
                graph.update(link)
                additions += 1
                break
        else:
            graphs.append(link)
            additions += 1
        graphs = join_graphs(graphs)
        if len(graphs) == 1 and len(graphs[0]) == len(data):
            return prod(data[x][0] for x in link)
            break
    


#% -------------------------------------------

if __name__ == "__main__":
    do_timing = False
    
    file_path_example = os.path.join(script_path, 'example_input.txt')
    if os.path.isfile(file_path_example):
        print(f"Task with example inputs:")
        task_1_success = execute_function(
            task_1,
            args = {'input_path': file_path_example, 'n_links': 10},
            do_timing = do_timing,
            solution = 40
        )
        
        task_2_success = execute_function(
            task_2,
            args = {'input_path': file_path_example},
            do_timing = do_timing,
            solution = 25272
        )
        
    
        file_path = os.path.join(script_path, 'input.txt')
        if os.path.isfile(file_path):
            print(f"Task with real inputs:")
            if task_1_success:
                execute_function(
                    task_1,
                    args = {'input_path': file_path},
                    do_timing = do_timing,
                    solution = 54180
                )
            
            if task_2_success:
                execute_function(
                    task_2,
                    args = {'input_path': file_path},
                    do_timing = do_timing,
                    solution = 25325968
                )

# Task with example inputs:
# Function: task_1
# 	Result: 40
# 	Execution time: 0.0000 ms.
# 	✔️ CORRECT!
# Function: task_2
# 	Result: 25272
# 	Execution time: 5.9566 ms.
# 	✔️ CORRECT!
# Task with real inputs:
# Function: task_1
# 	Result: 54180
# 	Execution time: 3.3824 s.
# 	✔️ CORRECT!
# Function: task_2
# 	Result: 25325968
# 	Execution time: 38.6613 s.
# 	✔️ CORRECT!