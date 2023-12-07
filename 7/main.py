# %%
import pandas as pd
import numpy as np

# %% 1
# pd.read_fwf pilasi elämäni ja luki tiedostosta arvon väärin 1000 -> 100
# Korttikäden tyypt saa rankattua logiikalla [suurimman ryhmän koko] - [ryhmien määrä]
# Korttikäden tyypin tasatilanteessa sorted funktio vertaa kortteja järjestyksessä: 
#   [käden arvo, kortin 1 arvo, kortin 2 arvo, ...]

print(sum(((i+1) * bet) for i, (_, cards, bet) in enumerate(sorted([(np.unique(list(hand), return_counts=True)[1], hand, bet) for hand, bet in pd.read_csv('input.txt', delim_whitespace=True, header=None).values], key = lambda groups_n_hand: (groups_n_hand[0].max()-groups_n_hand[0].size, *list(groups_n_hand[1].translate(str.maketrans('TJQKA', f'ABCDE'))))))))

# %% 2
# 1. Jätkille annetaan arvo 0
# 2. Jätkiä ei lasketa korttiryhmiin mukaan
# 3. Jokereiden määrä lisätään suurimpaan korttiryhmään
# 4. viiden jokerin tapauksessa käden arvo on 3. (Neljän suoran arvo on 2 ja viiden suoran arvo on 4)

print(sum((bet * (i+1)) for i, (_, cards, bet) in enumerate(sorted([(np.unique(list(hand.replace('J','')), return_counts=True)[1], hand, bet) for hand, bet in pd.read_csv('input.txt', delim_whitespace=True, header=None).values], key = lambda groups_n_hand: (3 if not groups_n_hand[0].size else groups_n_hand[0].max()-groups_n_hand[0].size+5-groups_n_hand[0].sum(), *list(groups_n_hand[1].translate(str.maketrans('TJQKA', f'A0CDE'))))))))

