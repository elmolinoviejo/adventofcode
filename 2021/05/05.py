from collections import Counter
import numpy as np


def read_input(fn):
    edges = []
    with open(fn) as fh:
        for line in fh.readlines():
            edge_locs = []
            for edge in line.split(' -> '):
                edge_locs.append(tuple([
                    int(x) for x in edge.split(',')]))
            edges.append(edge_locs)
    return edges


def check_diag(edge):
    (x1, y1), (x2, y2) = edge
    if (x1 != x2) & (y1 != y2):
        return True
    return False


def get_locs(edge, skipdiag=True):
    (x1, y1), (x2, y2) = edge
    dx = np.sign(x2 - x1)
    dy = np.sign(y2 - y1)

    if check_diag(edge):
        if skipdiag:
            return []
        locs = [(x, y) for x, y in zip(
            np.arange(x1, x2 + dx, dx),
            np.arange(y1, y2 + dy, dy))]

    elif x1 == x2:
        locs = [(x1, y) for y in np.arange(y1, y2 + dy, dy)]
    elif y1 == y2:
        locs = [(x, y1) for x in np.arange(x1, x2 + dx, dx)]

    return locs


def solve(edges, skipdiag=True):
    loc_counts = Counter()
    for edge in edges:
        locs = get_locs(edge, skipdiag)
        for loc in locs:
            loc_counts[loc] += 1

    ans = 0
    for k, v in loc_counts.items():
        if v > 1:
            ans += 1
    return ans


fn = '05.txt'
edges = read_input(fn)

print(solve(edges))
print(solve(edges, skipdiag=False))
