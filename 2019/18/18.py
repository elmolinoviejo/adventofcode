import numpy as np
# from numpy.linalg import lstsq
from copy import deepcopy
from collections import deque
from itertools import combinations
import string
import networkx as nx
import cProfile


class Vault():
    def __init__(self):
        self.halls = []
        self.current_loc = None
        self.start_loc = None
        self.end_loc = None
        self.key_locs = {}
        self.door_locs = {}
        self.remaining_keys = []
        # self.key_distances = dict()
        self.graph = nx.Graph()
        self.key_graph = nx.Graph()
        self.path_length = 0

    def build_graph(self):
        self.graph.add_nodes_from(self.halls)

        for loc, key in self.key_locs.items():
            self.graph.add_node(loc, key=key)
            self.remaining_keys.append(key)
            self.remaining_keys.sort()
            if key.upper() not in self.door_locs.values():
                self.end_loc = loc

        for x, y in self.graph.nodes:
            for adj in [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]:
                if adj in self.graph.nodes:
                    self.graph.add_edge((x, y), adj)

        for loc, door in self.door_locs.items():
            self.graph.add_node(loc, door=door)

    def build_key_graph(self):
        # Open all doors:
        key_distances = dict()
        for key_loc in self.key_locs.keys():
            self.open_door(key_loc)

        sub_nodes = [l for l in self.key_locs.keys()]
        sub_nodes.extend([self.start_loc])

        # Get all paths
        for loc1, loc2 in combinations(sub_nodes, r=2):
            shortest_path = nx.shortest_path(self.graph, loc1, loc2)
            path_keys = set([
                x for x in shortest_path if x in self.key_locs])
            path_not_locs = set([
                x for x in shortest_path if x not in [loc1, loc2]])
            if path_keys & path_not_locs:
                continue
            else:
                self.key_graph.add_edge(
                    loc1, loc2, weight=len(shortest_path) - 1)
                # self.key_distances[(loc1, loc2)] = len(shortest_path) - 1
                # self.key_distances[(loc2, loc1)] = len(shortest_path) - 1
                key_distances[(loc1, loc2)] = len(shortest_path) - 1
                key_distances[(loc2, loc1)] = len(shortest_path) - 1
        self.close_all_doors()
        return key_distances

    def get_next_keys(self):
        possible_next_key_locs = []
        remaining_key_locs = [
            kl for kl, k in self.key_locs.items() if k in self.remaining_keys]
        # print(remaining_key_locs)
        for key_loc in remaining_key_locs:
            if nx.has_path(self.graph, self.current_loc, key_loc):
                possible_next_key_locs.append(key_loc)
        possible_next_keys = [
            k for kl, k in
            self.key_locs.items() if
            kl in possible_next_key_locs]
        return possible_next_key_locs, possible_next_keys

    def open_door(self, key_loc):
        key = self.key_locs[key_loc]
        self.remaining_keys.remove(key)
        door = key.upper()
        self.current_loc = key_loc
        if door in self.door_locs.values():
            door_loc = [dl for dl, d in self.door_locs.items() if d == door][0]
            self.graph.add_node(door_loc)
            (x, y) = door_loc
            for adj in [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]:
                if adj in self.graph.nodes:
                    self.graph.add_edge((x, y), adj)

    def close_door(self, key_loc):
        key = self.key_locs[key_loc]
        self.remaining_keys.append(key)
        self.remaining_keys.sort()
        door = key.upper()
        if door in self.door_locs.values():
            door_loc = [dl for dl, d in self.door_locs.items() if d == door][0]
            if door_loc in self.graph.nodes:
                self.graph.remove_node(door_loc)

    def close_all_doors(self):
        for key_loc in self.key_locs:
            self.close_door(key_loc)

    def match_remaining_keys(self, remaining_keys):
        doors_to_open = set(self.remaining_keys) - set(
            remaining_keys)
        doors_to_open = [
            kl for kl, k in self.key_locs.items() if k in doors_to_open]
        doors_to_close = set(remaining_keys) - set(
            self.remaining_keys)
        doors_to_close = [
            kl for kl, k in self.key_locs.items() if k in doors_to_close]
        for key_loc in doors_to_open:
            self.open_door(key_loc)
        for key_loc in doors_to_close:
            self.close_door(key_loc)


def input_to_map(fn, vault):
    with open(fn, 'r') as fh:
        for y, l in enumerate(fh):
            for x, val in enumerate(l.rstrip()):
                if val == '.':
                    vault.halls.append((x, y))
                elif val in string.ascii_lowercase:
                    vault.key_locs[(x, y)] = val
                elif val in string.ascii_uppercase:
                    vault.door_locs[(x, y)] = val
                elif val == '@':
                    vault.current_loc = (x, y)
                    vault.start_loc = (x, y)
                    vault.halls.append((x, y))


def initialize(fn):
    vault = Vault()
    input_to_map(fn, vault)
    vault.build_graph()
    key_distances = vault.build_key_graph()
    vault.remaining_keys = [k for k in vault.key_locs.values()]
    vault.current_loc = vault.start_loc
    return vault, key_distances


def reset_vault(vault):
    vault.current_loc = vault.start_loc
    vault.close_all_doors()
    vault.remaining_keys = [k for k in vault.key_locs.values()]
    return vault


# Try memoizing vaults, instead of always opening and closing doors
def solver(fn):
    v, key_distances = initialize(fn)
    min_path_length = np.inf
    # pairwise_distances = dict()
    paths_to_test = deque([[v.start_loc]])
    checked_paths = {((v.start_loc),): deepcopy(v)}
    available_keys = dict()  # keys are remaining keys, values are key_locs
    available_keys[set(v.remaining_keys)] = set(v.get_next_keys()[0])
    long_paths = []
    # print(checked_paths)
    while paths_to_test:
    # while False:
    # for _ in range(1000):
        current_path = paths_to_test.pop()
        # Memoize vaults, instead of always opening and closing doors
        path_not_found = True
        path_to_calculate = []
        # print(checked_paths)
        # print(current_path)
        while path_not_found:
            if tuple(current_path) in long_paths:
                continue
            if tuple(current_path) in checked_paths:
                v = deepcopy(checked_paths[tuple(current_path)])
                path_not_found = False
                current_found_path = deepcopy(current_path)
            else:
                path_to_calculate.append(current_path.pop(-1))
        # go through the current path to caluculate
        if len(path_to_calculate) > 0:
            path_to_calculate.reverse()
            # print(current_found_path, v.path_length)
            # print(path_to_calculate)
            for loc_ind, loc in enumerate(path_to_calculate):
                if loc in v.key_locs:
                    v.open_door(loc)

            # Add last distance to path distance
            # First try finding if memoized
                if loc_ind == 0:
                    path_pair = (current_found_path[-1], loc)
                else:
                    path_pair = (path_to_calculate[loc_ind - 1], loc)
                if path_pair in key_distances:
                    # path_length += v.key_distances[path_pair]
                    v.path_length += key_distances[path_pair]
                else:
                    last_path_length = nx.dijkstra_path_length(
                        v.key_graph, path_pair[0], path_pair[1],
                        weight='weight')
                    key_distances[
                        path_pair] = last_path_length
                    key_distances[
                        (path_pair[1], path_pair[0])] = last_path_length
                    # path_length += last_path_length
                    v.path_length += key_distances[path_pair]

                # print(tuple(
                #     current_found_path + path_to_calculate))
                # print(v.path_length)
                checked_paths[tuple(
                    current_found_path + path_to_calculate)] = deepcopy(v)
                # print(checked_paths)

                if loc == v.end_loc and v.remaining_keys == []:
                    if v.path_length < min_path_length:
                        min_path_length = v.path_length
                        print(min_path_length)

        if set(v.remaining_keys) not in available_keys:
            next_key_locs, next_keys = v.get_next_keys()
            available_keys[set(v.remaining_keys)] = set(next_key_locs)
        else:
            next_key_locs = available_keys[set(v.remaining_keys)]

        if v.path_length > min_path_length:
            long_paths.append(
                tuple(current_found_path + path_to_calculate))
            del checked_paths[
                tuple(current_found_path + path_to_calculate)]
            continue

        for next_key_loc in next_key_locs:
            if next_key_loc not in current_path:
                paths_to_test.append(
                    current_found_path +
                    path_to_calculate +
                    [next_key_loc])


def solver2(fn):
    v, key_distances = initialize(fn)
    min_path_length = np.inf
    # min_path_length = 150
    paths_to_test = deque([[v.start_loc]])

    checked_path_distances = {((v.start_loc),): 0}
    checked_path_remaining_keys = {((v.start_loc),): set(v.remaining_keys)}
    # long_paths = []
    available_keys = dict()  # keys are remaining keys, values are key_locs
    available_keys[tuple(v.remaining_keys)] = v.get_next_keys()[0]
    # print(checked_paths)
    while paths_to_test:
    # while False:
    # for _ in range(500000):
        current_path = paths_to_test.pop()
        path_not_found = True
        skip_path = False
        path_to_calculate = []
        while path_not_found:
            if tuple(current_path) not in checked_path_distances:
                path_to_calculate.append(current_path.pop(-1))
            # print(checked_path_remaining_keys)
            current_path_to_check = deepcopy(current_path)
            current_path_to_check.sort()
            # print(tuple(current_path_to_check))
            remaining_keys = checked_path_remaining_keys[tuple(current_path_to_check)]
            v.path_length = checked_path_distances[
                tuple(current_path)]
            path_not_found = False
            current_found_path = current_path

            if False:
                pass
            else:
                # When do I need to actually match the opened/closed doors?
                v.match_remaining_keys(remaining_keys)

        if skip_path:
            print('skip')
            # never skips, because I never add the long paths to the queue!
            continue

        # go through the current path to calculate
        if len(path_to_calculate) > 0:
            path_to_calculate.reverse()
            for loc_ind, loc in enumerate(path_to_calculate):
                if loc in v.key_locs:
                    v.open_door(loc)
                if loc_ind == 0:
                    path_pair = (current_found_path[-1], loc)
                else:
                    path_pair = (path_to_calculate[loc_ind - 1], loc)
                if path_pair in key_distances:
                    v.path_length += key_distances[path_pair]
                else:
                    last_path_length = nx.dijkstra_path_length(
                        v.key_graph, path_pair[0], path_pair[1],
                        weight='weight')
                    key_distances[
                        path_pair] = last_path_length
                    key_distances[
                        (path_pair[1], path_pair[0])] = last_path_length
                    v.path_length += key_distances[path_pair]

                checked_path_distances[tuple(
                    current_found_path + path_to_calculate)] = v.path_length
                path_to_store = current_found_path + path_to_calculate
                path_to_store.sort()
                checked_path_remaining_keys[tuple(path_to_store)] = set(
                        v.remaining_keys)
                # print(checked_paths)
                if len(v.remaining_keys) == 0:
                    if v.path_length < min_path_length:
                        min_path_length = v.path_length
                        print(f'lowest path: {min_path_length}')
                        # for p, length in checked_path_distances.items():
                        #     if length > min_path_length:
                        #         long_paths.append(p)

        if tuple(v.remaining_keys) not in available_keys:
            next_key_locs, next_keys = v.get_next_keys()
            available_keys[tuple(v.remaining_keys)] = next_key_locs
        else:
            next_key_locs = available_keys[tuple(v.remaining_keys)]

        if v.path_length > min_path_length:
            # next_path = current_found_path + path_to_calculate

            continue
        else:
            for next_key_loc in next_key_locs:
                if next_key_loc not in current_path:
                    next_path = current_found_path + path_to_calculate + [next_key_loc]
                    # if tuple(next_path) not in long_paths:
                    paths_to_test.append(next_path)
        # print(len(paths_to_test))
        # [print(d) for d in checked_path_distances.values()]
    print(min_path_length)

fn = '18_test3.txt'
# v, key_distances = initialize(fn)
# x = deepcopy(v.remaining_keys)
# for key_loc in v.key_locs.keys():
#     v.open_door(key_loc)
# print(v.remaining_keys)
# v.match_remaining_keys(x)
# print(v.remaining_keys)

# cProfile.run('solver2(fn)')
solver2(fn)
