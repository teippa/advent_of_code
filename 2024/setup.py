#%%
main_template = """#%%

FILENAME = 'example_input.txt'
# FILENAME = 'input.txt'

def load_data(
    filename: str, 
    lines: bool = False, 
    matrix: bool = False,
    dtype: callable = str):
    
    with open(filename, 'r', encoding='utf-8') as file:
        if matrix:
            return [
                [dtype(char) for char in line.strip()]
                for line in file.readlines()
            ]
        if lines:
            return [
                dtype(line)
                for line in file.readlines()
            ]
        return file.read()
data = load_data(FILENAME)


def task_1(data):
    return

def task_2(data):
    return
    
if __name__ == "__main__":
    print('task_1:', task_1(data))

    print('task_2:', task_2(data))
    
"""
import os
from datetime import datetime as dt

script_path = os.path.dirname(os.path.abspath(__file__))


def main():
    now = dt.now()
    if now.month != 12:
        print(f"It's not X-mas time yet!")
        return
    today_dir_name = f"{now.day:0>2.0f}"
    today_dir_path = os.path.join(script_path, today_dir_name)
    if os.path.isdir(today_dir_path):
        print("Todays directory is already created.")
        return
    
    os.mkdir(today_dir_path)
    with open(os.path.join(today_dir_path, 'main.py'), 'a') as file:
        file.write(main_template)
    with open(os.path.join(today_dir_path, 'input.txt'), 'a') as file:
        pass
    with open(os.path.join(today_dir_path, 'example_input.txt'), 'a') as file:
        pass
    
    
if __name__ == "__main__":
    main()