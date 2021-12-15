from itertools import product

import networkx as nx


def load_input(fn):
    rls = {}
    with open(fn) as fh:
        for y, line in enumerate(fh.read().split('\n')):
            for x, rl in enumerate(line):
                rls[(x, y)] = int(rl)
    return rls


def get_adj(loc):
    x, y = loc
    adjs = []
    for dx, dy in product((-1, 0, 1), (-1, 0, 1)):
        if abs(dx) + abs(dy) == 1:
            adjs.append((x + dx, y + dy))
    return adjs


def make_graph(rls):
    G = nx.DiGraph()
    for loc in rls:
        for adj in get_adj(loc):
            if adj not in rls:
                continue
            G.add_edge(loc, adj, weight=rls[adj])
    return G


def get_ans(G):
    ans = 0
    sp = nx.dijkstra_path(G, (0, 0), max(G.nodes), weight='weight')
    for loc in sp:
        if loc == (0, 0):
            continue
        ans += rls[loc]
    return ans


def expand_rl(rls, xt=5, yt=5):
    rls_original = rls.copy()
    maxx, maxy = max(rls_original)
    for xt, yt in product(range(5), range(5)):
        if (xt, yt) == (0, 0):
            continue
        for loc, v in rls_original.items():
            x, y = loc

            new_v = (v + xt + yt)
            if new_v > 9:
                new_v = new_v % 9

            rls[(x + xt * (maxx + 1)),
                (y + yt * (maxy + 1))] = new_v
    return rls


fn = '15.txt'
rls = load_input(fn)
G = make_graph(rls)
print(get_ans(G))

rls2 = expand_rl(rls)
G2 = make_graph(rls2)
print(get_ans(G2))
