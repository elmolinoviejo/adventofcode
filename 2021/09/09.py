from collections import deque


def import_map_heights(fn):
    hs = {}
    with open(fn) as fh:
        for y, line in enumerate(fh.readlines()):
            for x, h in enumerate(line.rstrip()):
                hs[(int(x), int(y))] = int(h)
    return hs


def risk_level(loc, hs):
    return hs[loc] + 1


def get_adjs(loc, hs):
    x, y = loc
    adjs = []
    for adj in [(x + 1, y),
                (x - 1, y),
                (x, y + 1),
                (x, y - 1)]:
        if adj in hs:
            adjs.append(adj)
    return adjs


def check_low(loc, hs):
    h = hs[loc]
    for adj in get_adjs(loc, hs):
        if hs[adj] <= h:
            return False
    return True


def get_basin(loc, hs):
    basin = set()
    q = deque([loc])
    checked = set()
    while len(q) > 0:
        loc = q.popleft()
        checked.add(loc)
        if hs[loc] == 9:
            continue
        basin.add(loc)
        for adj in get_adjs(loc, hs):
            if (adj not in checked) and (adj not in q):
                q.append(adj)

    return basin


# fn = '09_test.txt'
fn = '09.txt'
hs = import_map_heights(fn)

# Part One
ans = 0
low_points = []
for loc in hs:
    if check_low(loc, hs):
        low_points.append(loc)
        ans += risk_level(loc, hs)
print(ans)

# Part Two
basins = []
for loc in low_points:
    basins.append(get_basin(loc, hs))
basins.sort(key=len, reverse=True)

prod = 1
for b in basins[:3]:
    prod = prod * len(b)

print(prod)
