#%%
import numpy as np
import matplotlib.pyplot as plt

with open("input.txt", 'r') as F:
    patterns = [
        np.array([
            list(line)
            for line in structure.split('\n')
        ])
        for structure in F.read().strip().split("\n\n")
    ]

# def mirror_detector(arr):
#     zero_positions = np.argwhere(np.abs(arr) < 2).flatten()
#     results = []
#     for zp in zero_positions:
#         is_mirror = True
#         smudge_found = arr[zp] == 1
#         for i in range(1,arr.size):
#             a, b = zp-i, zp+i
#             if a < 0 or arr.size <= b:
#                 break
#             # print(arr[a], arr[b])
#             if smudge_found < 2 and abs(arr[a] + arr[b]) == 1:
#                 smudge_found += 1
#             elif smudge_found == 1:
#                 # Tää smudge 1 2 on ihan typerää, 
#                 # mutta ku se voi vaikuttaa kahen 
#                 # peräkkäisen rivin/sarakkeen diffeihin
#                 # ja en jaksa ajatella parempaa ratkasua...
#                 # Just look away
#                 smudge_found += 1
#             elif arr[a] != -1*arr[b]:
#                 is_mirror = False
#                 break

            
#         results.append([is_mirror, smudge_found>0, zp+1])
    
#     if results:
#         return max(results)
#     else:
#         return [False, False, 0]
    
def mirror_detector(pattern):
    differences = np.diff(pattern=='#', axis=0).sum(axis=1)
    zero_positions = np.argwhere(np.abs(differences) < 2).flatten()
    for zp in zero_positions:
        is_valid_mirror = True
        smudge_detected = False

        print(differences)

        for i in range(differences.size-1):
            a, b = zp-i, zp+i+1
            if a < 0 or differences.size <= b:
                break
            rows = np.array([pattern[a,:], pattern[b,:]])
            print(rows)






total = 0
for p in patterns[12:]:
    plt.imshow(p=='#')
    plt.show()

    v = mirror_detector(p)
    # h = mirror_detector(p.transpose())

    # horizontal_differences = np.diff(p=='#', axis=0).sum(axis=1)
    # # vertical_differences = 

    

    # print(horizontal_differences, vertical_differences)
    
    # h = mirror_detector(horizontal_differences)
    # v = mirror_detector(vertical_differences)

    # if (h[0] and v[0]):
    #     print("pakssa")
    # # print(v,h)
    # print(h[0] or v[0])
    # print(h,  v)
    
    # if h[1] > 0 and v[1] > 0:
    #     h[1] *= h[0]
    #     v[1] *= v[0]
        
    # total += 100*h[1] + v[1]

    break
    
total

# %%
