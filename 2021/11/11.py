from itertools import product


def get_octs(fn):
    octs = {}
    with open(fn) as fh:
        for y, line in enumerate(fh.readlines()):
            for x, o in enumerate(line.rstrip()):
                octs[(x, y)] = int(o)
    return octs


def get_adj(loc, octs):
    x, y = loc
    adjs = []
    for dx, dy in product([-1, 0, 1], [-1, 0, 1]):
        adj = (x + dx, y + dy)
        if adj == loc:
            continue
        elif adj not in octs:
            continue
        adjs.append(adj)
    return adjs


def step(octs):
    for loc in octs:
        octs[loc] += 1

    n_flash = 0
    flashed = set()
    n_to_flash = len(
        [o for loc, o in octs.items() if (o > 9) and (loc not in flashed)])
    while n_to_flash > 0:
        for loc, o in octs.items():
            if o > 9:
                if loc in flashed:
                    continue
                n_flash += 1
                flashed.add(loc)
                octs[loc] = 0
                for adj in get_adj(loc, octs):
                    if adj in flashed:
                        continue
                    octs[adj] += 1
        n_to_flash = len(
            [o for loc, o in octs.items() if (o > 9) and (loc not in flashed)])
    return octs, n_flash


fn = '11.txt'

octs = get_octs(fn)
ans = 0
for _ in range(100):
    octs, nf = step(octs)
    ans += nf
print(ans)


octs = get_octs(fn)
s = 0
while True:
    octs, nf = step(octs)
    s += 1
    if nf == 100:
        print(s)
        break
