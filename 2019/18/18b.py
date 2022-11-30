# from collections import deque
from heapq import heappush, heappop
from itertools import combinations
import string

import networkx as nx


class Vault:
    def __init__(self):
        self.halls = []
        # self.start_loc = None
        self.key_locs = {}   # dict of keys: locations
        self.loc_keys = {}   # dict of locations: keys
        self.door_locs = {}  # dict of doors: locations
        self.loc_doors = {}  # dict of locations: doors
        self.full_graph = nx.Graph()
        self.key_graph = nx.Graph()

    def input_to_map(self, fn, part=1):
        with open(fn, 'r') as fh:
            for y, l in enumerate(fh):
                for x, val in enumerate(l.rstrip()):
                    if val == '.':
                        self.halls.append((x, y))
                    elif val in string.ascii_lowercase:
                        self.key_locs[val] = (x, y)
                        self.loc_keys[(x, y)] = val
                    elif val in string.ascii_uppercase:
                        self.door_locs[val.lower()] = (x, y)
                        self.loc_doors[(x, y)] = val.lower()
                    elif val == '@':
                        if part == 1:
                            # self.start_loc = (x, y)
                            self.halls.append((x, y))
                            self.loc_keys[(x, y)] = '@'
                        elif part == 2:
                            sl = (x, y)
        if part == 2:
            # self.start_loc = []
            sx, sy = sl

            for ind, loc in enumerate([
                (sx - 1, sy - 1),
                (sx + 1, sy - 1),
                (sx - 1, sy + 1),
                (sx + 1, sy + 1)
            ]):
                # self.start_loc.append(loc)
                self.loc_keys[loc] = str(ind)
                if loc not in self.halls:
                    self.halls.append(loc)

            for loc in [
                (sx, sy - 1),
                (sx - 1, sy),
                (sx, sy),
                (sx + 1, sy),
                (sx, sy + 1)
            ]:
                if loc in self.halls:
                    self.halls.remove(loc)

    def build_graph(self):
        self.full_graph.add_nodes_from(self.halls)

        for key, loc in self.key_locs.items():
            self.full_graph.add_node(loc)

        for door, loc in self.door_locs.items():
            self.full_graph.add_node(loc)

        for x, y in self.full_graph.nodes:
            for adj in [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]:
                if adj in self.full_graph.nodes:
                    self.full_graph.add_edge((x, y), adj)

    def build_key_graph(self):
        # ideas: just use keys as nodes. list doors between keys
        self.build_graph()
        sub_nodes = [loc for loc in self.loc_keys]
        for loc1, loc2 in combinations(sub_nodes, r=2):
            if not nx.has_path(self.full_graph, loc1, loc2):
                continue
            shortest_path = nx.shortest_path(self.full_graph, loc1, loc2)
            keys_in_path = set()
            doors_in_path = set()
            for node in shortest_path:
                if node in [loc1, loc2]:
                    continue
                if node in sub_nodes:
                    keys_in_path.add(self.loc_keys[node])
                if node in self.loc_doors:
                    doors_in_path.add(self.loc_doors[node])
            self.key_graph.add_edge(
                self.loc_keys[loc1],
                self.loc_keys[loc2],
                weight=len(shortest_path) - 1,
                doors=doors_in_path,
                keys=keys_in_path)
        return self.key_graph


def shortest_path_bfs(kg):
    # key_min_dist = dict()
    h = []
    heappush(h, (0, '@', '@'))
    # h.append(tuple([0, '@', '@']))
    min_dist = 1E10
    while h:
        pdist, p, n1 = heappop(h)

        if set(p) == set(kg.nodes):
            if pdist < min_dist:
                min_dist = pdist
                print(pdist, p, n1)
            continue

        for n2 in kg.nodes:
            if (n2 == n1) or (n2 in p):
                continue

            edoors = kg.edges[n1, n2]['doors']
            if not edoors.issubset(p):
                continue

            new_dist = pdist + kg.edges[n1, n2]['weight']
            if new_dist > min_dist:
                continue

            ekeys = kg.edges[n1, n2]['keys']
            new_p = p + n2
            # print(''.join([k for k in ekeys]))
            new_p += ''.join([k for k in ekeys])
            new_p = ''.join(sorted(set(new_p)))

            # if (new_p, n2) not in key_min_dist:
            #     key_min_dist[new_p] = new_dist
            # elif new_dist > key_min_dist[(new_p, n2)]:
            #     continue

            heappush(h, (new_dist, new_p, n2))
            # h.append(tuple([new_dist, new_p, n2]))
            # print(h[0])
            # print(len(h))
    print(min_dist)


def shortest_path_dfs(kg):
    # memoize shortest path for keys (any order)
    # keys_mindist = dict()
    h = []
    # heappush(h, (0, '@', '@'))

    h.append(tuple([0, '@', '@']))
    min_dist = 1E6
    while h:
        pdist, p, n1 = heappop(h)

        # if pdist >= min_dist:
        #     continue

        if set(p) == set(kg.nodes):
            if pdist < min_dist:
                min_dist = pdist
                print(min_dist, len(h))
                # print(pdist, p, n1)
            continue

        while set(p) != set(kg.nodes):
            next_p = []
            to_check = kg.nodes

            for n2 in to_check:
                # print(n1, n2)

                if (n2 == n1) or (n2 in p):
                    continue

                edoors = kg.edges[n1, n2]['doors']
                if not edoors.issubset(p):
                    continue

                new_dist = pdist + kg.edges[n1, n2]['weight']
                if new_dist > min_dist:
                    continue

                ekeys = kg.edges[n1, n2]['keys']
                new_p = p + n2
                new_p += ''.join([k for k in ekeys])
                new_p = ''.join(sorted(set(new_p)))

                # if new_p in keys_mindist:
                #     if new_dist > keys_mindist[new_p]:
                #         continue
                #     if new_dist < keys_mindist[new_p]:
                #         keys_mindist[new_p] = new_dist

                next_p.append(tuple([new_dist, new_p, n2]))

            next_p = sorted(next_p, reverse=True)
            if len(next_p) == 0:
                # if pdist < min_dist:
                #     min_dist = pdist
                #     print(min_dist)
                break
            # print(next_p)
            pdist, p, n1 = next_p.pop()
            # [heappush(h, x) for x in next_p]
            [h.append(x) for x in next_p] 
            # print(h)

        else:
            if pdist < min_dist:
                min_dist = pdist
                print(min_dist, len(h))
        # print(min_dist)
    print(min_dist)


def shortest_path_dfs_p2(kg):
    # memoize shortest path for keys (any order)
    # keys_mindist = dict()
    h = []
    # heappush(h, (0, '@', '@'))

    h.append(tuple([0, '0123', '0123']))
    min_dist = 2379
    while h:
        pdist, p, n1s = heappop(h)

        # if pdist >= min_dist:
        #     continue

        if set(p) == set(kg.nodes):
            if pdist < min_dist:
                min_dist = pdist
                print(min_dist, len(h))
                # print(pdist, p, n1)
            continue

        while set(p) != set(kg.nodes):
            next_p = []
            to_check = kg.nodes

            for n1 in n1s:
                for n2 in to_check:
                    # print(n1, n2)

                    if (n2 == n1) or (n2 in p):
                        continue

                    if not nx.has_path(kg, n1, n2):
                        continue

                    edoors = kg.edges[n1, n2]['doors']
                    if not edoors.issubset(p):
                        continue

                    new_dist = pdist + kg.edges[n1, n2]['weight']
                    if new_dist > min_dist:
                        continue

                    ekeys = kg.edges[n1, n2]['keys']
                    new_p = p + n2
                    new_p += ''.join([k for k in ekeys])
                    new_p = ''.join(sorted(set(new_p)))

                    n2s = n1s.replace(n1, n2)
                    # print(n1s, n2s)
                    next_p.append(tuple(
                        [new_dist, new_p, n2s]))

            next_p = sorted(next_p, reverse=True)
            if len(next_p) == 0:
                break

            # print(next_p)
            pdist, p, n1s = next_p.pop()
            # [heappush(h, x) for x in next_p]
            [h.append(x) for x in next_p]
            # print(h)

        else:
            if pdist < min_dist:
                min_dist = pdist
                print(min_dist, len(h))
        # print(h)
        # print(min_dist)
    print(min_dist)


# V = Vault()
# V.input_to_map('18.txt')
# kg = V.build_key_graph()
# shortest_path_dfs(kg)


# 4410 wrong
# 4406 right

# Part 2

V = Vault()
# V.input_to_map('18.txt', part=2)
V.input_to_map('18.txt', part=2)
kg = V.build_key_graph()
# print(V.loc_keys)
shortest_path_dfs_p2(kg)

# 2378 too high

