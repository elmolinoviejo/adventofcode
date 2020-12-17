from itertools import product


def load_map(fn, dimensions=3):
    locs = {}
    for r, line in enumerate(open(fn).read().split('\n')):
        for c, val in enumerate(line):
            if val == '#':
                if dimensions == 3:
                    locs[(r, c, 0)] = val
                elif dimensions == 4:
                    locs[(r, c, 0, 0)] = val

    return locs


def get_neighbors(loc, dimensions=3):
    ns = []
    for diffs in product([-1, 0, 1], repeat=dimensions):
        n = [0] * dimensions
        for ind, (l, d) in enumerate(zip(loc, diffs)):
            n[ind] = l + d
        ns.append(tuple(n))
    ns.remove(loc)
    return ns


def step_isactive(loc, locs, dimensions):
    n_active = 0
    if loc not in locs:
        val = '.'
    else:
        val = locs[loc]
    for n in get_neighbors(loc, dimensions):
        if n not in locs:
            continue
        elif locs[n] == '#':
            n_active += 1

    if (val == '#') and (1 < n_active < 4):
        return True
    elif (val == '.') and (n_active == 3):
        return True
    else:
        return False


def step(locs, dimensions=3):
    new_locs = {}
    # check each loc and each neighbor
    checked = set()
    for loc, val in locs.items():
        if step_isactive(loc, locs, dimensions):
            new_locs[loc] = '#'
        checked.add(loc)
        for n in get_neighbors(loc, dimensions):
            if n not in checked:
                checked.add(n)
                if step_isactive(n, locs, dimensions):
                    new_locs[n] = '#'
    return new_locs


runs = {'Part 1': 3, 'Part 2': 4}
for part, dim in runs.items():
    locs = load_map('17.txt', dim)
    for _ in range(6):
        locs = step(locs, dimensions=dim)
    print(f"{part}:\t{sum([v=='#' for v in locs.values()])}")
