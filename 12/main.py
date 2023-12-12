# %%
from collections import Counter
from itertools import permutations
import matplotlib.pyplot as plt
from tqdm import tqdm

#%%

def parse_line(line):
    springs, ranges = line.strip().split(' ')
    return springs, [int(i) for i in ranges.split(',')]

def springs2list(springs: str):
    return [int(i) for i in springs.translate(str.maketrans('.?#', '012'))]

with open("input.txt", 'r') as F:
    lines = F.readlines()

kamalaa = 0
for line in tqdm(lines):
    springs, palikat = parse_line(line)


    used = sum(palikat) # Tässä palkoiden viemä tila 

    # Tässä pisteille jäävä tila, yks piste palikoiden väleistä aina pois,
    # koska palikoiden välissä on pakko olla piste defaulttina niinku
    unused = len(springs) - used - (len(palikat) - 1) 

    voi_helvetti = 0 # Validit järjestelyt jne

    # 🤮🤮🤮🤮🤮🤮🤮🤮🤮 Hyi, tää pilaa kaiken, tulee liikaa tavaraa ulos
    for bobs in Counter(permutations([*palikat + [0,] * unused])).keys():

        # Joo tässä skipataan jos ne palikat on väärässä järjestyksessä
        if any(x[0]!=x[1] for x in zip(palikat, [b for b in bobs if b])):
            continue
        
        # Sitte lisätää pisteitä sinne palikoiden välii ja ympärille
        # Ja tehää niistä palikoista kans oikeita palikoita jne
        paskaa = ''
        added = 0
        for b in bobs:

            if b:
                if added == 1:
                    # Tää on tärkee
                    paskaa += '.'
                paskaa += '#'*b
                added = 1
            else:
                paskaa += '.'
        
        
        if all(p[0] == p[1] or p[0] == '?' for p in zip(springs, paskaa)):
            # print(paskaa)
            voi_helvetti += 1
        
    # print(voi_helvetti)

    kamalaa += voi_helvetti


print(kamalaa)


# %%

