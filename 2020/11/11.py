from collections import Counter
from itertools import product


def input_to_vals(fn):
    vals = {}
    lines = [g for g in open(fn).read().split('\n')]
    for r, line in enumerate(lines):
        for c, val in enumerate(line):
            vals[(r, c)] = val
    return vals


def calc_adjacent(vals):
    dirs = product([-1, 0, 1], repeat=2)
    dirs = [d for d in dirs if d != (0, 0)]
    adjacents = {}
    for loc in vals.keys():
        adj = []
        r, c = loc
        for d in dirs:
            a = (r + d[0], c + d[1])
            if a in vals:
                adj.append(a)
        adjacents[loc] = adj
    return adjacents


def calc_visible(vals):
    dirs = product([-1, 0, 1], repeat=2)
    dirs = [d for d in dirs if d != (0, 0)]
    visibles = {}
    for loc in vals.keys():
        r, c = loc
        vis = []
        for d in dirs:
            end = False
            r1, c1 = r, c
            while not end:
                next_loc = (r1 + d[0], c1 + d[1])
                if next_loc in vals:
                    if vals[next_loc] in 'L#':
                        vis.append(next_loc)
                        end = True
                else:
                    end = True
                r1, c1 = next_loc
        visibles[loc] = vis
    return visibles


def step(vals, adjacents, n_seats=1):
    new_vals = {}
    n_changes = 0
    for loc, val in vals.items():
        adj_vals = [vals[x] for x in adjacents[loc]]
        if (val == 'L') and ('#' not in adj_vals):
            new_vals[loc] = '#'
            n_changes += 1
        elif (val == '#') and (Counter(adj_vals)['#'] > n_seats):
            new_vals[loc] = 'L'
            n_changes += 1
        else:
            new_vals[loc] = val
    return new_vals, n_changes


def print_map(vals):
    max_x = max([x for (x, y) in vals.keys()])
    max_y = max([y for (x, y) in vals.keys()])
    output = ''
    for x in range(max_x + 1):
        output += '\n'
        for y in range(max_y + 1):
            output += vals[(x, y)]
    print(output)


# Part A
printout = False
vals = input_to_vals('11.txt')
adjacents = calc_adjacent(vals)
n_changes = 1
while n_changes != 0:
    if printout:
        print(print_map(vals))
        print(n_changes)
    vals, n_changes = step(vals, adjacents, 3)
print(f"Part 1:\t{Counter(list(vals.values()))['#']}")


# Part 2
printout = False
vals = input_to_vals('11.txt')
visibles = calc_visible(vals)
n_changes = 1
while n_changes != 0:
    if printout:
        print(print_map(vals))
        print(n_changes)
    vals, n_changes = step(vals, visibles, 4)
print(f"Part 2:\t{Counter(list(vals.values()))['#']}")
