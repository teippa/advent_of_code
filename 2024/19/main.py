# https://adventofcode.com/2024/day/19
#%% ----------- SETUP -------------------------
from itertools import chain
import os
import re
from sys import path as SYSPATH

from tqdm import tqdm

script_path = os.path.dirname(os.path.abspath(__file__))

SYSPATH.append(os.path.join(script_path, '..'))
from utils import load_data, execute_function

#%--------- THE IMPORTANT STUFF -------------

FILENAME = 'example_input.txt'
FILENAME = 'input.txt'
file_path = os.path.join(script_path, FILENAME)

def loader_i_hardly_know_her():
    towels_str, patterns_str = load_data(file_path).strip().split('\n\n')
    patterns = sorted(
        (pat.strip() for pat in patterns_str.split('\n')),
        key = len
    )
    towels = sorted(
        (tow.strip() for tow in towels_str.split(',')),
        key=len,
        reverse=True
    )
    one_colors = {tow for tow in towels if len(tow) == 1}
    filtered_towels = tuple(
        tow
        for tow in towels
        if not all(c in one_colors for c in tow)
    )
    
    # return towels, patterns
    return one_colors, filtered_towels, patterns

def bad_idea(one_colors, towel_patterns, patterns):
    """ This does not work because of overlaps
    """
    cans = 0
    fails = []
    repl = lambda x: 'X'*len(x)
    for pat in patterns:
        patpat = str(pat) # I don't know
        # print(patpat)
        for tp in towel_patterns:
            patpat = re.sub(tp, repl(tp), patpat)
            # print('\t'+patpat)
        for tp in one_colors:
            patpat = re.sub(tp, 'X', patpat)
            # print('\t'+patpat)
        if all(c=='X' for c in patpat):
            cans += 1
        else:
            fails.append(pat)
    
    return cans, fails

all_colors = set('rbgwu')

def finder_I_hardly_know_her(arr, key, neg_key = None):
    """ index of thiny that makes the key true, etc., etc., etc.
    """
    for i, val in enumerate(arr):
        if key(val):
            return i
        elif neg_key is not None and neg_key(val):
            # we can give up early if we want.
            # Useful because the array is ordered
            return None
    return None

def do_thing(target: int, rems: list[tuple], current: tuple[int,int] = None):

    if current is None:
        # print(len(rems))
        first = rems[0]
        index = finder_I_hardly_know_her(
            rems, 
            key=lambda x: x[0]>first[0]
        )
        branches = rems[:index]
        new_rems = rems[index:]
        # print('branch', branches, new_rems)
        for branch_current in branches:
            good_branch = do_thing(target, new_rems, branch_current)
            if good_branch:
                return True
        else:
            return False
    else:
        if current[1] == target:
            return True
        # print(current, rems)
        end = current[1]
        ind = finder_I_hardly_know_her(
            rems, 
            key=lambda x: end==x[0],
            neg_key=lambda x: x[0]>end
        )
        if ind is not None:
            # This is good
            return do_thing(target, rems[ind:])
        else:
            return False

from  matplotlib import pyplot as plt
import numpy as np
def removals2image(removals, pattern):
    im = np.zeros((len(removals), len(pattern)))
    for i, rem in enumerate(removals):
        im[i, slice(*rem)] = 1
    plt.imsave('bad_pattern_ims/'+pattern+'.png', im)
    
    

def aggobaggo(towels, pattern):
    good_things_happening = True
    shift = lambda tpl, n: tuple(t+n for t  in tpl)
    removals = []
    # print(pattern)
    for tp in towels:
        for i in range(len(pattern)):
            m = re.match(tp, pattern[i:])
            if m is not None:
                removals.append(shift(m.span(), i))
    removals.sort(key=lambda x: (x[0], -x[1]))
    # print(len(removals))
    
    # Test for gaps in removals
    i_max = 0
    for r in removals:
        if r[0] > i_max:
            good_things_happening = False
        i_max = max(i_max, r[1])
    if i_max < len(pattern):
        good_things_happening = False
    
    if good_things_happening:
        good_things_happening = do_thing(len(pattern), removals)
    if not good_things_happening:
        removals2image(removals, pattern)
    return good_things_happening

def task_1():
    one_colors, towel_patterns, patterns = loader_i_hardly_know_her()
    towels = (*one_colors, *towel_patterns)
    # asdasd = []
    # for i in range(1, len(towels)-1):
    #     towels[:-i]
    #     p = towels[-i]
    #     if not aggobaggo(towels, p):
    #         asdasd.append(p)
    
    # print(sorted(asdasd, key=len))
        
    
    # good_things, fails = bad_idea(one_colors, towel_patterns, patterns)
    good_things = 0
    # print(one_colors, towel_patterns, patterns)
    for pat in tqdm(patterns):
        # print(f"{i}/{len(fails)}")
        # if pat != 'brgwgubrugwrguwuruubwgbggbwwwgguwwbgwguburgugruwgbruwbgwwg':
        #     continue
        is_good = aggobaggo(towels, pat)
        if is_good:
            good_things += 1
        # break
    
    return good_things
        
        
    

def task_2():
    data = load_data(file_path)
    return



#% -------------------------------------------

if __name__ == "__main__":
    do_timing = False
    execute_function(
        task_1,
        args = {},
        do_timing = do_timing
    )
    
    execute_function(
        task_2,
        args = {},
        do_timing = do_timing
    )
    
# %%
