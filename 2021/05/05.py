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


def get_locs(edge, skipdiag=False):
    (x1, y1), (x2, y2) = edge

    if check_diag(edge) and skipdiag:
        continue

    # change to use sign of difference
    if x1 < x2:
        dx = 1
    elif x1 > x2:
        dx = -1

    if y1 < y2:
        dy = 1
    elif y1 > y2:
        dy = -1

    if x1 == x2:
        locs = [(x1, y) for y in np.arange(y1, y2 + dy, dy)]
    if y1 == y2:
        locs = [(x, y1) for x in np.arange(x1, x2 + dx, dx)]


    elif check_diag(edge):

    else:
        if y1 == y2:
            locs = [(x, y1) for x ]

fn = '05.txt'
els = read_input(fn)
print(els)
