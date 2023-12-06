# advent_of_code_2023
 
Testaillaan miten ~~monimutkaisesti~~ elegantisti voi asioita koodailla... sillon kun jaksaa ja ehtii ja osaa.


## Mitä opin?

Välilyönneillä erotettuja taulukoita on helppo lukea pandasilla:
``` python
pandas.read_csv(
    'input.txt', 
    delim_whitespace=True, 
    header=None, # Otsikot pois
    index_col=[0,] # Rivien nimet pois
)
pandas.read_fwf('input.txt', header=None, index_col=[0,])
```

