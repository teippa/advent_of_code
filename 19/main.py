# %%
import re

with open("script.py", 'w') as script, open("input.txt", 'r') as F:
    script.write("def A(obj):\n\treturn obj\n")
    script.write("def R(obj = None):\n\treturn {}\n\n")
    lines = iter(F.readlines())
    for line in lines:
        if not line.strip():
            break
        line = line.replace('in', 'main')
        asd = re.split(r'[{},:]',line)[:-1]
        bo = ''
        bo += f"def {asd[0]}(obj):\n\t"
        bo += f"x,m,a,s = obj['x'], obj['m'], obj['a'], obj['s']\n\t"
        for i in range(1,len(asd)-1, 2):
            cond, res = asd[i:i+2]
            bo += f"if({cond}):\n\t\treturn {res}(obj)\n\tel"
        bo += f"se:\n\t\treturn {asd[-1]}(obj)\n\n"
        script.write(bo)
    
    script.write("\n\nobjs = [\n")
    for line in lines:
        line = line.replace("=", ":")
        line = line.replace("x", "'x'")
        line = line.replace("m", "'m'")
        line = line.replace("a", "'a'")
        line = line.replace("s", "'s'")
        script.write(f"\t{line.strip()},\n")
    script.write("]\n\n")

    script.write( "if __name__ == '__main__':\n")
    script.write(f"\tprint(sum(sum(main(obj).values()) for obj in objs if obj))\n")
    
from script import main, objs

if __name__ == '__main__':
    # print(objs)
    print(sum(sum(main(obj).values()) for obj in objs if obj))

