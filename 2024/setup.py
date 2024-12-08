#%%
import os
from datetime import datetime as dt

script_path = os.path.dirname(os.path.abspath(__file__))

def touch(file_path):
    with open(file_path, 'a') as _:
        pass

def main():
    now = dt.now()
    if now.month != 12:
        print(f"It's not X-mas time yet!")
        return
    today_dir_name = f"{now.day:0>2.0f}"
    today_dir_path = os.path.join(script_path, today_dir_name)
    
    try:
        os.mkdir(today_dir_path)
    except FileExistsError as e:
        print("Todays directory is already created.")
        return
        
    with open(os.path.join(today_dir_path, 'main.py'), 'a') as file, \
         open(os.path.join(script_path, 'template.py'), 'r') as template_file:
        file.write(f"# https://adventofcode.com/{now.year}/day/{now.day}\n")
        file.write(template_file.read())
    touch(os.path.join(today_dir_path, 'input.txt'))
    touch(os.path.join(today_dir_path, 'example_input.txt'))
    
    
if __name__ == "__main__":
    main()