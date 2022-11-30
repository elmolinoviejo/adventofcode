import re
from itertools import product
# from scipy.ndimage import center_of_mass
import numpy as np
from collections import deque


def load_bots(fn):
    bots = {}
    lines = [x for x in open(fn).read().split('\n')]
    for line in lines:
        pos = re.search(r'\<([\-\d\,]*)\>', line)[1]
        pos = tuple([int(x) for x in pos.split(',')])
        radius = int(line.split('=')[-1])
        bots[pos] = radius
    return bots


def dist(b1, b2):
    return sum([abs(x1 - x2) for x1, x2 in zip(b1, b2)])


def num_in_range(loc, bots):
    n = 0
    for b2 in bots:
        d = dist(loc, b2)
        if d <= bots[b2]:
            n += 1
    return n


def bot_overlap(b1, b2, bots):
    d = dist(b1, b2)
    if bots[b1] + bots[b2] <= d:
        return True
    else:
        return False


def desc_adj(loc, step=1):
    x, y, z = loc
    adj = []
    for dx, dy, dz in product([0, -1 * step, step],
                              repeat=3):
        if dx == dy == dz == 0:
            continue
        adj.append(tuple([x - dx,
                          y - dy,
                          z - dz]))
    return adj


def find_max_locs(to_check, tested, maxval, bots, step):
    max_locs = to_check
    while to_check:
        loc = to_check.pop()
        tested.add(loc)
        for adj in desc_adj(loc, step=step):
            if adj in tested:
                continue

            nir = num_in_range(adj, bots)
            if nir < maxval:
                tested.add(adj)
                continue
            elif nir > maxval:
                maxval = nir
                # print(nir, dist(adj, (0, 0, 0)))
                max_locs = [adj]
                to_check.append(adj)
            else:
                to_check.append(adj)
                max_locs.append(adj)
        # print(len(to_check))

    return max_locs, maxval, tested


bots = load_bots('23test2.txt')  # pos: radius
bots = load_bots('23.txt')  # pos: radius


bots_in_range = dict()
for b in bots:
    bots_in_range[b] = num_in_range(b, bots)

maxval = max(bots_in_range.values())


to_check = [k for k, v in bots_in_range.items()
            if v == maxval]
tested = set()

step = 1000000
# step = 10
for _ in range(10):
    max_locs, maxval, tested = find_max_locs(
        to_check, tested, maxval, bots, step=step)

    for m in max_locs:
        print(dist(m, (0, 0, 0)))

    to_check = max_locs
    step = step / 10



#  5658529 too low
#  8944674 too low
# 42611322 too low
# 43947521 wrong 
# 46281258 wrong
# 46279329 wrong
# 45748547 wrong



# bots_list = list(bots.keys())
# bots_overlap = dict()
# for b1, b2 in zip(bots_list, bots_list[1:]):
#     if bot_overlap(b1, b2, bots):
#         for b in [b1, b2]:
#             if b not in bots_overlap:
#                 bots_overlap[b] = set()

#         bots_overlap[b1].add(b2)
#         bots_overlap[b2].add(b1)


# print(bots_overlap)
# max_in_range = max([len(v) for v in bots_overlap.values()])
# # print(max_in_range)
# start_locs = [k for k, v in bots_overlap.items()
#               if len(v) == max_in_range]
# print(start_locs)

# for b in bots:
#     print(b, num_in_range(b, bots))
