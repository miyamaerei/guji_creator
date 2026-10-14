import io, os
os.chdir(r"E:\git\ToolBox\guji\mingshi\mingshi-zhiguanzhi\scripts")
s = io.open("_struct_ai_01.py", encoding="utf-8").read()
i = s.index("LINES = [")
lines = s[i:].split("\n")
for k, ln in enumerate(lines, 1):
    print("%3d| %s" % (k, ln))
