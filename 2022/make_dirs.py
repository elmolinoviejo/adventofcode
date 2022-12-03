import os

for d in range(1, 26):
    dname = f"{d:02d}"
    fname = f"{dname}/{dname}.txt"
    sname = f"{dname}/{dname}.py"

    try:
        os.mkdir(dname)
    except:
        pass

    with open(fname, 'w'):
        pass

    with open(sname, 'w'):
        pass
