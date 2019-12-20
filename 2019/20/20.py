import numpy as np
import string
import networkx as nx


def parse_map(fn):
    passages = []
    labels = dict()
    with open(fn, 'r') as fh:
        for y, l in enumerate(fh):
            for x, char in enumerate(l.rstrip()):
                if char == '.':
                    passages.append((x, y))
                if char in string.ascii_uppercase:
                    labels[(x, y)] = char
    return passages, labels


def get_portal_locs(labels, passages):
    portal_locs = dict()
    for (x, y), letter in labels.items():
        if (x + 1, y) in labels:
            portal_name = letter + labels[(x + 1, y)]
            if (x + 2, y) in passages:
                portal_loc = (x + 2, y)
            elif (x - 1, y) in passages:
                portal_loc = (x - 1, y)
        elif (x, y + 1) in labels:
            portal_name = letter + labels[(x, y + 1)]
            if (x, y + 2) in passages:
                portal_loc = (x, y + 2)
            elif (x, y-1) in passages:
                portal_loc = (x, y - 1)

        else:
            continue

        if portal_name not in portal_locs:
            portal_locs[portal_name] = [portal_loc]
        else:
            portal_locs[portal_name].append(portal_loc)

    return portal_locs


def get_portal_locs_level(labels, passages):
    x_max = max([x for x, y in passages])
    y_max = max([y for x, y in passages])

    outer_portal_locs = dict()
    inner_portal_locs = dict()
    for (x, y), letter in labels.items():
        if (x + 1, y) in labels:
            portal_name = letter + labels[(x + 1, y)]
            if (x + 2, y) in passages:
                portal_loc = (x + 2, y)
            elif (x - 1, y) in passages:
                portal_loc = (x - 1, y)

            if x == 0 or x >= x_max - 2:
                outer = True
            else:
                outer = False

        elif (x, y + 1) in labels:
            portal_name = letter + labels[(x, y + 1)]
            if (x, y + 2) in passages:
                portal_loc = (x, y + 2)
            elif (x, y-1) in passages:
                portal_loc = (x, y - 1)

            if y == 0 or y >= y_max - 2:
                outer = True
            else:
                outer = False
        else:
            continue

        if outer:
            outer_portal_locs[portal_name] = portal_loc
        else:
            inner_portal_locs[portal_name] = portal_loc

    return outer_portal_locs, inner_portal_locs


def make_graph(g, passages, portal_locs):
    for (x, y) in passages:
        for adj in [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]:
            if adj in passages:
                g.add_edge((x, y), adj)

    for label, locs in portal_locs.items():
        if label in ['AA', 'ZZ']:
            continue
        else:
            g.add_edge(locs[0], locs[1])


def make_graph_recursive(g, passages, outer_portal_locs, inner_portal_locs, recurse=1):
    if g.nodes:
        previous_level = max([n[2] for n in g.nodes])
    else:
        previous_level = 0
    for level in np.arange(previous_level, recurse):
        for (x, y) in passages:
            for adj in [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]:
                if adj in passages:
                    g.add_edge((x, y, level), (adj[0], adj[1], level))

        if level + 1 <= recurse:
            for label, locs in inner_portal_locs.items():
                if label in ['AA', 'ZZ']:
                    continue
                else:
                    inner_loc = (locs[0], locs[1], level)
                    outer_loc = (outer_portal_locs[label][0], outer_portal_locs[label][1], level+1)
                    g.add_edge(inner_loc, outer_loc)

print('Part A')
fn = '20.txt'

g = nx.Graph()
passages, labels = parse_map(fn)
portal_locs = get_portal_locs(labels, passages)
start_loc = portal_locs['AA'][0]
end_loc = portal_locs['ZZ'][0]

make_graph(g, passages, portal_locs)
print(nx.shortest_path_length(g, start_loc, end_loc))

print('Part B')
fn = '20.txt'
g2 = nx.Graph()
passages, labels = parse_map(fn)
outer_portal_locs, inner_portal_locs = get_portal_locs_level(labels, passages)
start_loc = (outer_portal_locs['AA'][0], outer_portal_locs['AA'][1], 0)
end_loc = (outer_portal_locs['ZZ'][0], outer_portal_locs['ZZ'][1], 0)

has_path = False
recurse = 2
while not has_path:
    print(f'level: {recurse}')
    make_graph_recursive(g2, passages, outer_portal_locs, inner_portal_locs, recurse)
    has_path = nx.has_path(g2, start_loc, end_loc)
    recurse += 1
print(nx.shortest_path_length(g2, start_loc, end_loc))
