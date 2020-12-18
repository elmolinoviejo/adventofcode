import networkx as nx
from itertools import combinations


def calc_erosion_level(coord, erosion_levels, depth):
    y, x = coord
    if y == 0 and x == 0:
        gi = 0
    elif y == 0:
        gi = x * 16807
    elif x == 0:
        gi = y * 48271
    else:
        gi = erosion_levels[(y, x - 1)] * erosion_levels[(y - 1, x)]
    el = (gi + depth) % 20183
    erosion_levels[coord] = el
    return erosion_levels


def calc_type(erosion_levels):
    types = dict()
    for coord, l in erosion_levels.items():
        types[coord] = l % 3
    return types


def map_types(depth, t_loc, edge_buffer):
    erosion_levels = {}
    for x in range(0, t_loc[1] + 1 + edge_buffer):
        for y in range(0, t_loc[0] + 1 + edge_buffer):
            if (y, x) == t_loc:
                erosion_levels[t_loc] = erosion_levels[(0, 0)]
            else:
                erosion_levels = calc_erosion_level((y, x),
                                                    erosion_levels,
                                                    depth)
    types = calc_type(erosion_levels)
    return types


def make_graph(types):
    type_tools = {0: 'tc', 1: 'cn', 2: 'tn'}
    G = nx.Graph()
    # Add all nodes with permissible tools
    for loc in types.keys():
        x, y = loc
        G.add_nodes_from([(loc, t) for t in type_tools[types[loc]]
                          if (loc, t) not in G])
    # Add edges
    for loc in types:
        # Add edges for switching tools in place
        for toolpair in combinations('tcn', 2):
            t1, t2 = toolpair
            if ((loc, t1) in G) and ((loc, t2) in G):
                if t1 == t2:
                    weight = 1
                else:
                    weight = 7
                G.add_edge((loc, t1), (loc, t2), weight=weight)
        # Add edges for moving if same tool
        x, y = loc
        for adj in [(x - 1, y), (x + 1, y),
                    (x, y - 1), (x, y + 1)]:
            for t in 'tcn':
                if ((loc, t) in G) and ((adj, t) in G):
                    G.add_edge((loc, t), (adj, t), weight=1)
    return G


depth = 10914
t_loc = (739, 9)  # (y, x) coord

# Test Data
# depth = 510
# t_loc = (10, 10)

# Part 1
edge_buffer = 0
types = map_types(depth, t_loc, edge_buffer)
t_sum = sum(types.values())
print(f"Part 1:\t{t_sum}")

# Part 2
edge_buffer = 100
types = map_types(depth, t_loc, edge_buffer)
G = make_graph(types)
ans = nx.shortest_path_length(G, ((0, 0), 't'), (t_loc, 't'), weight='weight')
print(f"Part 2:\t{ans}")
