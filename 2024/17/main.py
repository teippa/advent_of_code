# https://adventofcode.com/2024/day/17
#%% ----------- SETUP -------------------------
from itertools import zip_longest
import os
import re
from sys import path as SYSPATH

from tqdm import tqdm

script_path = os.path.dirname(os.path.abspath(__file__))

SYSPATH.append(os.path.join(script_path, '../..'))
from utils import load_data, execute_function

#%--------- THE IMPORTANT STUFF -------------

FILENAME = 'example_input.txt'
FILENAME = 'input.txt'
file_path = os.path.join(script_path, FILENAME)

def loadthething():
    data = load_data(file_path)
    progggei = tuple(map(int, re.search(r'Program: (.*?)[\n$]', data).groups(1)[0].split(',')))
    regisksd = dict(zip('abc', (int(abc) for abc in re.findall(r'[ABC]: (\d+)\n', data))))
    # very cool
    return progggei, regisksd
        

prog, regs = loadthething()
# prog = [5,0,5,1,5,4]
# regs = dict(zip('abc', [10,0,0]))
output = []
ip=0 # instruev pooibter
combos= [
    lambda: 0,
    lambda: 1,
    lambda: 2,
    lambda: 3,
    lambda: regs['a'],
    lambda: regs['b'],
    lambda: regs['c'],
    lambda: 1/0
]
def adv(x):
    regs['a'] = int(regs['a'] / (2**combos[x]()))
def bxl(x):
    regs['b'] = regs['b'] ^ x
def bst(x):
    regs['b'] = combos[x]()%8
def jnz(x):
    if regs['a'] != 0:
        global ip
        ip = x-2
def bxc(x):
    combos[x]()
    regs['b'] = regs['b'] ^ regs['c']
def out(x):
    """The out instruction (opcode 5) 
        calculates the value of its combo operand 
        modulo 8, then outputs that value. 
        (If a program outputs multiple values, they are separated by 
        commas.)"""
    output.append(combos[x]()%8)
def bdv(x):
    regs['b'] = int(regs['a'] / (2**combos[x]()))
def cdv(x):
    regs['c'] = int(regs['a'] / (2**combos[x]()))
    
insts = [
    adv,
    bxl,
    bst,
    jnz,
    bxc,
    out,
    bdv,
    cdv,
]
def ip_fwd(ip):
    return ip + 2
def task_1():
    global ip, output
    ip = 0
    output = []
    while True:
        try:
            inst_i = prog[ip]
            the_other_i = prog[ip+1]
            # print(ip, inst_i, the_other_i, combos[the_other_i](), regs)
        except IndexError:
            break
        insts[inst_i](the_other_i)
        ip = ip_fwd(ip)
    return ','.join(map(str, output))
    
    

def task_2():
    global ip, output
    for i in tqdm(range(100_000_000)):
        ip = 0
        output = []
        regs['a'] = i
        regs['b'] = 0
        regs['c'] = 0 
        
        iters = 0
        while len(output) < len(prog):
            iters += 1
            if iters > 100_000_000:
                print("iters over maybe too many")
                break
            try:
                inst_i = prog[ip]
                the_other_i = prog[ip+1]
                # print(ip, inst_i, the_other_i, combos[the_other_i](), regs)
            except IndexError:
                break
            insts[inst_i](the_other_i)
            ip = ip_fwd(ip)
        if all(a==b for a,b in zip_longest(output, prog, fillvalue=None)):
            return i



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
    