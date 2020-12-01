import numpy as np
# from numpy.linalg import lstsq
from copy import deepcopy
from collections import deque
from itertools import combinations
import string
import networkx as nx
import cProfile


class Vault:
    def __init__(self):
        self.halls = []
        self.start_loc = None
        self.key_locs = {}  # dict of keys: locations
        self.loc_keys = {}  # dict of locations: keys
        self.door_locs = {}  # dict of doors: locations
        self.remaining_keys = ''  # list of unopened key/doors
        self.door_edges = {}  # dict of doors: all edges
        self.key2key_distances = {}  # dict of dicts
        self.full_graph = nx.Graph()
        self.key_graph = nx.Graph()
        self.open_key_graph = nx.Graph()

    def input_to_map(self, fn):
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
                    elif val == '@':
                        self.start_loc = (x, y)
                        self.halls.append((x, y))

    def build_graph(self):
        self.full_graph.add_nodes_from(self.halls)

        for key, loc in self.key_locs.items():
            self.full_graph.add_node(loc)
            self.remaining_keys += key
        self.remaining_keys = ''.join(sorted(self.remaining_keys))

        for door, loc in self.door_locs.items():
            self.full_graph.add_node(loc)

        for x, y in self.full_graph.nodes:
            for adj in [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]:
                if adj in self.full_graph.nodes:
                    self.full_graph.add_edge((x, y), adj)

        for door, loc in self.door_locs.items():
            self.full_graph.add_node(loc)

    def build_key_graph(self):
        self.build_graph()
        sub_nodes = []
        sub_nodes.extend([loc for loc in self.key_locs.values()])
        sub_nodes.extend([loc for loc in self.door_locs.values()])
        sub_nodes.append(self.start_loc)

        for loc1, loc2 in combinations(sub_nodes, r=2):
            shortest_path = nx.shortest_path(self.full_graph, loc1, loc2)
            sub_nodes_in_path = set(
                [node for node in shortest_path if node in sub_nodes])
            sub_nodes_in_path.remove(loc1)
            sub_nodes_in_path.remove(loc2)
            if sub_nodes_in_path:
                continue
            else:
                self.key_graph.add_edge(
                    loc1, loc2, weight=len(shortest_path) - 1)

        for door, door_loc in self.door_locs.items():
            self.door_edges[door] = []
            for adj in self.key_graph.adj[door_loc]:
                self.door_edges[door].append((
                    door_loc, adj,
                    self.key_graph[door_loc][adj]['weight']))

        self.open_key_graph = deepcopy(self.key_graph)

    def open_door(self, door):
        for edge in self.door_edges[door]:
            self.key_graph.add_edge(edge[0], edge[1], weight=edge[2])


    def close_all_doors(self):
        for door, edges in self.door_edges.items():
            for edge in edges:
                try:
                    self.key_graph.remove_edge(edge[0], edge[1])
                except nx.exception.NetworkXError:
                    continue

    def get_accessible_keys(self, open_doors):
        remaining_keys = [
            k for k in self.key_locs.keys() if k not in open_doors]
        # Open doors
        for key in self.key_locs.keys():
            if key not in remaining_keys:
                if key in self.door_edges:
                    new_edges = self.door_edges[key]
                    for edge in new_edges:
                        self.key_graph.add_edge(edge[0], edge[1], weight=edge[2])

        accessible_keys = set()
        for key, key_loc in self.key_locs.items():
            if nx.has_path(self.key_graph, self.start_loc, key_loc):
                # accessible_keys.append(key)
                path_locs = [x for x in nx.shortest_path(
                    self.key_graph, self.start_loc, key_loc)]
                path_locs = path_locs[1:]  # remove start
                for path_loc in path_locs:
                    if path_loc in self.loc_keys:
                        if self.loc_keys[path_loc] not in open_doors:
                            accessible_keys.add(self.loc_keys[path_loc])
                            break
        accessible_keys = ''.join(sorted(list(accessible_keys)))

        return accessible_keys

    def get_key2key_distances(self, open_doors):
        accessible_keys = self.get_accessible_keys(open_doors)
        # print(f'O.D.s: {open_doors}')
        # print(f'func A.K.s: {accessible_keys}')
        self.key2key_distances[open_doors] = dict()

        keys_to_check = open_doors + accessible_keys
        # print(keys_to_check)

        for key1, key2 in combinations(keys_to_check, r=2):
            if '@' in [key1, key2]:
                continue
            dist = nx.dijkstra_path_length(
                self.key_graph, self.key_locs[key1], self.key_locs[key2],
                weight='weight')
            self.key2key_distances[open_doors][key1 + key2] = dist
            self.key2key_distances[open_doors][key2 + key1] = dist
            # print(key1, key2, dist)

        for key1 in keys_to_check:
            if key1 == '@':
                continue
            dist = nx.dijkstra_path_length(
                self.key_graph, self.key_locs[key1], self.start_loc,
                weight='weight')
            self.key2key_distances[open_doors][key1 + '@'] = dist
            self.key2key_distances[open_doors]['@' + key1] = dist
            # print(key1, dist)

        self.close_all_doors()
        return accessible_keys


def write_path(path, path_length, fn):
    with open(fn, 'a+') as fh:
        fh.write(f'{path}\t{path_length}\n')


def initialize_vault(fn):
    vault = Vault()
    vault.input_to_map(fn)
    vault.build_key_graph()
    # vault.get_key2key_distances('@')
    vault.close_all_doors()

    return vault


def solver(fn):
    v = initialize_vault(fn)
    min_path_length = np.inf
    # min_path_length = 140
    # min_path_length = 5476
    paths_to_test = deque(['@'])
    path_distances = dict()
    path_accessible_keys = dict()
    path_distances[('@', '@')] = 0
    path_accessible_keys['@'] = v.get_key2key_distances('@')
    # long_paths = set()

    with open(fn[:-4] + '_paths.txt', 'w+') as fh:
        fh.write('')

    while paths_to_test:
    # while False:
    # for _ in range(2):
        current_path = paths_to_test.pop()
        sorted_path = ''.join(sorted(current_path))
        last_loc = current_path[-1]
        continue_path = True

        if (sorted_path, last_loc) not in path_distances:
            path_distances[(sorted_path, last_loc)] = np.inf

        # memoize accessible keys, and path lengths
        if sorted_path in path_accessible_keys:
            accessible_keys = path_accessible_keys[sorted_path]
            # v.key2key_distances
        else:
            accessible_keys = v.get_key2key_distances(sorted_path)
            path_accessible_keys[sorted_path] = accessible_keys
            # print(f'acc. keys: {accessible_keys}')
        # print(v.key2key_distances)
        # print(path_accessible_keys)

        path_length = 0
        for ind, key in enumerate(current_path):
            if ind == 0:
                continue

            path_length += v.key2key_distances[sorted_path][
                current_path[ind - 1] + key]
        # print(current_path, path_length)
        subpath_long = path_length > path_distances[
            (sorted_path, last_loc)]
        path_long = path_length > min_path_length
        if subpath_long or path_long:
            continue_path = False
            continue

        else:
            path_distances[(sorted_path, last_loc)] = path_length
            continue_path = True

        if len(current_path) == len(v.key_locs) + 1:
            if path_length < min_path_length:
                min_path_length = path_length
                write_path(
                    current_path,
                    path_length,
                    fn[:-4] + '_paths.txt')
                print(f'shortest path: {min_path_length}')

        elif continue_path:
            for key in accessible_keys:
                if key not in current_path:
                    next_path = current_path + key
                    paths_to_test.append(next_path)
        # print(paths_to_test)
    print(f'No. of path distances: {len(path_distances)}')
    print(f'No. of accessible keys: {len(path_accessible_keys)}')
    print(v.key2key_distances)
    print(min_path_length)
    print(v.key_graph)
    # print(long_paths)


fn = '18_test5.txt'
solver(fn)
# cProfile.run('solver(fn)')

# 5844 too high
# 5476 too high
# 4886 wrong... too high!
# 4302 wrong... too low!
