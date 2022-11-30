from itertools import product


def load_input(fn):
    '''
    Load reboot steps from file
    '''
    rbs = []
    with open(fn) as fh:
        for line in fh.read().split('\n'):
            status, coords = line.split(' ')
            x, y, z = coords.split(',')
            ds = []
            for d in [x, y, z]:
                ds.append(tuple(int(x) for x in d.split('=')[1].split('..')))
            rbs.append(tuple([status, tuple(ds)]))
    return rbs


def step_restrict(rb, onset):
    '''
    Perform reboot step with volume restriction
    '''
    status, ds = rb
    (x1, x2), (y1, y2), (z1, z2) = ds
    x1 = max(x1, -50)
    y1 = max(y1, -50)
    z1 = max(z1, -50)

    x2 = min(x2, 50)
    y2 = min(y2, 50)
    z2 = min(z2, 50)
    for loc in product(range(x1, x2 + 1),
                       range(y1, y2 + 1),
                       range(z1, z2 + 1)):
        if status == 'on':
            onset.add(loc)
        else:
            onset.discard(loc)
    return onset


def n_overlap(d1, d2):
    '''
    Number of overlapping voxels between two cuboids
    '''
    (x1, x2), (y1, y2), (z1, z2) = d1
    (a1, a2), (b1, b2), (c1, c2) = d2

    n = (max(min(a2, x2) - max(a1, x1), 0) *
         max(min(b2, y2) - max(b1, y1), 0) *
         max(min(c2, z2) - max(c1, z1), 0))

    return n


def is_within(d1, d2):
    '''
    True if d1 is within d2
    '''
    (x1, x2), (y1, y2), (z1, z2) = d1
    (a1, a2), (b1, b2), (c1, c2) = d2

    for dim in range(3):
        if min(d1[dim]) < min(d2[dim]):
            return False
        if max(d1[dim]) > max(d2[dim]):
            return False
    return True


def check_overlap(d1, d2):
    (x1, x2), (y1, y2), (z1, z2) = d1
    (a1, a2), (b1, b2), (c1, c2) = d2

    n = (max(min(a2, x2) - max(a1, x1), 0) *
         max(min(b2, y2) - max(b1, y1), 0) *
         max(min(c2, z2) - max(c1, z1), 0))

    if n > 0:
        return True
    else:
        return False


def split_overlap(d1, d2):
    (x1, x2), (y1, y2), (z1, z2) = d1
    (a1, a2), (b1, b2), (c1, c2) = d2

    locs = {}
    locs['x'] = (x1, x2, a1, a2)
    locs['y'] = (y1, y2, b1, b2)
    locs['z'] = (z1, z2, c1, c2)

    edges = dict()
    for dim in 'xyz':
        edges[dim] = []
        edges[dim].append(
            tuple(
                [min(locs[dim][0], locs[dim][2]),
                 max(locs[dim][0], locs[dim][2]) - 1]))

        edges[dim].append(
            tuple(
                [max(locs[dim][0], locs[dim][2]),
                 min(locs[dim][1], locs[dim][3])]))

        edges[dim].append(
            tuple(
                [min(locs[dim][1], locs[dim][3]) + 1,
                 max(locs[dim][1], locs[dim][3])]))

    cuboids = []
    for x, y, z in product(edges['x'], edges['y'], edges['z']):
        cuboids.append((x, y, z))
    # print(cuboids)

    overlaps = ([], [], [])
    for c in cuboids:
        in_d1 = is_within(c, d1)
        in_d2 = is_within(c, d2)
        if in_d1 and not in_d2:
            overlaps[0].append(c)
        if in_d2 and not in_d1:
            overlaps[1].append(c)
        if in_d1 and in_d2:
            overlaps[2].append(c)

    return overlaps


# fix this to return fewer cuboids (combine similar ones)
def gen_new_cuboids(rb1, rb2):
    s1, d1 = rb1
    s2, d2 = rb2
    overlaps = split_overlap(d1, d2)

    outrbs = []
    if len(overlaps[2]) > 0:
        overlap = True
    else:
        overlap = False
    for ind, cuboids in enumerate(overlaps):
        if ind == 0:
            if len(cuboids) == 0:
                outrbs.append(rb1)
            else:
                outrbs.extend((s1, c) for c in cuboids)
        elif ind == 1:
            if len(cuboids) == 0:
                outrbs.append(rb2)
            else:
                outrbs.extend((s2, c) for c in cuboids)
        else:
            outrbs.extend((s2, c) for c in cuboids)

    return outrbs, overlap


def reduce_cuboids(rbs):
    outrbs = []
    while rbs:
        rb1 = rbs.pop()
        s1, (x1, y1, z1) = rb1
        for rb2 in rbs:
            s2, (x2, y2, z2) = rb2
            if s1 == s2:
                if sum([x1 == x2,
                        y1 == y2,
                        z1 == z2]) > 1:
                    newrb = (s1,
                             (((min(*x1, *x2), max(*x1, *x2))),
                              ((min(*y1, *y2), max(*y1, *y2))),
                              ((min(*z1, *z2), max(*z1, *z2)))))
                    if rb2 in rbs:
                        rbs.remove(rb2)
                    if newrb in rbs:
                        rbs.remove(newrb)
                    # rbs.remove(rb2)
                    if newrb not in outrbs:
                        outrbs.append(newrb)
                    continue

            if rb1 not in outrbs:
                outrbs.append(rb1)
            if rb2 not in outrbs:
                outrbs.append(rb2)
    return outrbs


def remove_identical(rbs):
    cbset = set()
    rbsout = []
    while rbs:
        s, c = rbs.pop()
        if c in cbset:
            continue
        else:
            cbset.add(c)
            rbsout.append((s, c))
    rbsout.reverse()
    return rbsout


fn = '22_test.txt'
rbs = load_input(fn)

# Part One
# onset = set()
# for rb in rbs:
#     onset = step_restrict(rb, onset)
# print(f'Part One: {len(onset)}')


# Part Two

rb1 = ('on', [(3, 4), (3, 4), (3, 4)])
rb2 = ('on', [(0, 3), (0, 3), (0, 3)])

# print(rb1, rb2)
# overlaps = split_overlap(rb1[1], rb2[1])
# print(overlaps)
newcs, _ = gen_new_cuboids(rb1, rb2)
[print(x) for x in newcs]
print()
newcs = reduce_cuboids(newcs)
print(len(newcs))
[print(x) for x in newcs]

# rbs = rbs[:2]


# rbsout = []
# print(rbsout)
# overlaps = True
# # while overlaps:
# for _ in range(2):
#     overlaps = False
#     for rb2 in rbs:
#         if len(rbsout) == 0:
#             rbsout.append(rb2)
#         else:
#             for rb1 in rbsout:
#                 new_cs, ol = gen_new_cuboids(rb1, rb2)
#                 if ol:
#                     overlaps = True
#                 rbsout.extend(new_cs)
#                 print(len(rbsout))
#                 rbsout = remove_identical(rbsout)
#                 print(len(rbsout))
#                 print()
#     rbs = rbsout
#     rbsout = []

# [print(x) for x in rbs]





# Tests

# print(rbs[0])
# within
# rb1 = ('on', [(1, 3), (3, 1), (1, 3)])
# rb2 = ('on', [(1, 3), (1, 3), (1, 3)])
# print(is_within(rb1[1], rb2[1]))


# get all cubiods
# ---------------
# within
# rb1 = ('on', [(1, 2), (1, 2), (1, 2)])
# rb2 = ('on', [(0, 3), (0, 3), (0, 3)])

# overlaps = split_overlap(rb1[1], rb2[1])
# [print(x) for x in overlaps]
# print(len(overlaps[0]), len(overlaps[1]), len(overlaps[2]))


# # # one corner
# rb1 = ('on', [(3, 4), (3, 4), (3, 4)])
# rb2 = ('on', [(0, 3), (0, 3), (0, 3)])

# overlaps = split_overlap(rb1[1], rb2[1])
# [print(x) for x in overlaps]
# print(len(overlaps[0]), len(overlaps[1]), len(overlaps[2]))


# # one edge
# rb1 = ('on', [(0, 3), (3, 5), (3, 5)])
# rb2 = ('on', [(0, 3), (0, 3), (0, 3)])

# overlaps = split_overlap(rb1[1], rb2[1])
# [print(x) for x in overlaps]
# print(len(overlaps[0]), len(overlaps[1]), len(overlaps[2]))


# # none
# rb1 = ('on', [(4, 5), (4, 5), (4, 5)])
# rb2 = ('on', [(0, 3), (0, 3), (0, 3)])

# overlaps = split_overlap(rb1[1], rb2[1])
# [print(x) for x in overlaps]
# print(len(overlaps[0]), len(overlaps[1]), len(overlaps[2]))

# # # identical
# rb1 = ('on', ((0, 1), (0, 1), (0, 1)))
# rb2 = ('off', ((0, 1), (0, 1), (0, 1)))


# overlaps = split_overlap(rb1[1], rb2[1])
# # [print(x) for x in overlaps]
# print(len(overlaps[0]), len(overlaps[1]), len(overlaps[2]))

# outrbs = gen_new_cuboids(rb1, rb2)
# [print(x) for x in outrbs]

# remove_identical(outrbs)