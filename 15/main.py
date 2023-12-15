
# Determine the ASCII code for the current character of the string.
# Increase the current value by the ASCII code you just determined.
# Set the current value to itself multiplied by 17.
# Set the current value to the remainder of dividing itself by 256.


#%%
from itertools import accumulate
from collections import deque, OrderedDict
import re

# inputs = "rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7".split(',')
inputs = [s for s in open("input.txt", 'r').read().strip().split(',')]


def char_hash(current_value, char):
    return ((current_value + ord(char))*17)%256

def str_hash(string):
    return deque(accumulate(list(string), char_hash, initial=0), maxlen=1).pop()

# %%

hash_sum = sum(str_hash(i) for i in inputs)
print(f"{hash_sum = }") # 1320  521341

# %%

def get_lens_instructions(string):
    label = re.sub(r"[=-][0-9]?",'', string)
    focal = int(string[-1]) if string[-1].isnumeric() else 0
    return (
        str_hash(label),
        label,
        focal,
    )

def box_filling(inputs):
    boxes = [OrderedDict() for _ in range(256)]
    for box, label, focal in [get_lens_instructions(i) for i in inputs]:
        replace = boxes[box].get(label, 0) != 0
        boxes[box][label] = focal
        if not replace:
            boxes[box].move_to_end(label, last=True)
    return [
        {
            k: v 
            for k, v in box.items() 
            if v > 0
        } for box in boxes
    ]

def lens_values(boxes):
    return (
        (box_i+1)*(lens_i+1)*focal
        for box_i, box in enumerate(boxes)
        for lens_i, focal in enumerate(box.values())
    )
    

full_boxes = box_filling(inputs)
result = sum(lens_values(full_boxes))

print(f"{result = }") # 252782


# %%
