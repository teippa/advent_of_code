#%%
main_template = """#%%
from pandas import read_fwf as reader

FILENAME = 'example_input.txt'
# FILENAME = 'input.txt'

def load_data(filename: str, header: int = None):
    return reader(filename, header=None).values
data = load_data(FILENAME)


def main():
    return
    
if __name__ == "__main__":
    main()

"""
import os
from datetime import datetime as dt



def main():
    now = dt.now()
    if now.month != 12:
        print(f"It's not X-mas time yet!")
        return
    today_dir = f"{now.day:0>2.0f}"
    if os.path.isdir(today_dir):
        print("Todays directory is already created.")
        return
    
    os.mkdir(today_dir)
    with open(os.path.join(today_dir, 'main.py'), 'a') as file:
        file.write(main_template)
    with open(os.path.join(today_dir, 'input.txt'), 'a') as file:
        pass
    with open(os.path.join(today_dir, 'example_input.txt'), 'a') as file:
        pass
    
    
if __name__ == "__main__":
    main()