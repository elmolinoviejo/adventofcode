def get_input(fn):
    with open(fn) as fh:
        locs = [int(x) for x in fh.read().rstrip().split(',')]
        return locs


def lin_dist(l1, l2, lookup=None):
    dist = abs(l1 - l2)
    return dist


def nonlin_dist(l1, l2, lookup):
    dist = lookup[abs(l1 - l2)]
    return dist


def min_fuel(locs, dist_func=lin_dist):
    min_dist = 1E9
    for l1 in range(max(locs)):
        dist = 0
        for l2 in locs:
            dist += dist_func(l1, l2, lookup)
        if dist < min_dist:
            min_dist = dist
    return min_dist


locs = get_input('07.txt')

lookup = {0: 0}
for d in range(max(locs) + 1):
    if d > 0:
        lookup[d] = lookup[d - 1] + d

print(min_fuel(locs, lin_dist))
print(min_fuel(locs, nonlin_dist))
