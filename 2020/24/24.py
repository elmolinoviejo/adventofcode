def get_steps(line):
    steps = []
    skip = False
    for ind, s in enumerate(line):
        if skip:
            skip = False
            continue
        elif s in 'ns':
            steps.append(s + line[ind + 1])
            skip = True
        else:
            steps.append(s)
    return steps


def get_adjacent(loc):
    diffs = [(1, 0, -1), (0, 1, -1),
             (-1, 1, 0), (-1, 0, 1),
             (0, -1, 1), (1, -1, 0)]
    adj = []
    for diff in diffs:
        adj.append(tuple([x + d for x, d in zip(loc, diff)]))
    return adj


def load_steplist(fn):
    steplist = []
    for line in [g for g in open(fn).read().split('\n')]:
        steplist.append(get_steps(line))
    return steplist


def move_and_flip(steps, black_tiles):
    diffs = [(1, 0, -1), (0, 1, -1),
             (-1, 1, 0), (-1, 0, 1),
             (0, -1, 1), (1, -1, 0)]
    directions = ['e', 'se', 'sw', 'w', 'nw', 'ne']
    step_diffs = dict(zip(directions, diffs))

    loc = (0, 0, 0)
    for ind, s in enumerate(steps):
        diff = step_diffs[s]
        loc = tuple([x + d for x, d in zip(loc, diff)])
        if ind == len(steps) - 1:
            if loc in black_tiles:
                black_tiles.remove(loc)
            else:
                black_tiles.append(loc)
    return black_tiles


def flip_tiles(black_tiles, neighbors):
    new_black_tiles = set()
    checked_white = set()
    for loc in black_tiles:
        # lookup or generate neighbors
        if loc not in neighbors:
            ns = get_adjacent(loc)
            neighbors[loc] = set(ns)
        else:
            ns = neighbors[loc]

        # check if black tile stays black
        b_count = len([n for n in ns if n in black_tiles])
        if b_count in (1, 2):
            new_black_tiles.add(loc)
        # check if adjacent white tiles switch to black
        for nloc in ns:
            if nloc in checked_white:
                continue
            if nloc not in neighbors:
                n_ns = get_adjacent(nloc)
                neighbors[nloc] = set(n_ns)
            else:
                n_ns = neighbors[nloc]

            if nloc in black_tiles:
                continue

            checked_white.add(nloc)
            nb_count = len([nb for nb in n_ns if nb in black_tiles])
            if nb_count == 2:
                new_black_tiles.add(nloc)
    return new_black_tiles, neighbors


fn = '24.txt'
steplist = load_steplist(fn)

# Part 1
black_tiles = []
for steps in steplist:
    black_tiles = move_and_flip(steps, black_tiles)
print(f"Part 1:\t{len(black_tiles)}")

# Part 2
neighbors = {}
black_tiles = set(black_tiles)
for _ in range(100):
    black_tiles, neighbors = flip_tiles(black_tiles, neighbors)
print(f"Part 2:\t{len(black_tiles)}")
