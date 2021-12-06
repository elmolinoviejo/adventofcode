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


def get_locs(edge):
    (x1, y1), (x2, y2) = edge
    if check_diag(edge):
        continue
    else:
        if x1 > x2:
            xa = x1
            xb = x2 - 1
            step = -1
        elif x1 < x2:
            xa = x1
            xb = x2 + 1
            step = 1
        for x in np.arange(x1, x2 - 1, -1):
            locs.append(x, y1)
        else:
            for x in 

fn = '05.txt'
els = read_input(fn)
print(els)
