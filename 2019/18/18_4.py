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
        # self.door_locs = {} # dict of doors: locations
        # self.loc_doors = {} # dict of locations: doors
        self.full_graph = nx.Graph()
        self.key_graph = nx.Graph()

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
                        self.loc_doors[(x, y)] = val.lower()
                    elif val == '@':
                        self.start_loc = (x, y)
                        self.halls.append((x, y))

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
        sub_nodes = [self.start_loc]
        sub_nodes.extend([loc for loc in self.key_locs.values()])
        # sub_nodes.extend([loc for loc in self.door_locs.values()])

        for loc1, loc2 in combinations(sub_nodes, r=2):
            shortest_path = nx.shortest_path(self.full_graph, loc1, loc2)
            keys_in_path = set()
            doors_in_path = ''
            for node in shortest_path:
                if node in sub_nodes:
                    keys_in_path.add(node)
                if node in self.loc_doors:
                    doors_in_path += self.loc_doors[node]
            # keys_in_path = set(
            #     [node for node in shortest_path if node in sub_nodes])
            # doors_in_path = set(
            #     [node for node in shortest_path if node in self.door_locs.])
            keys_in_path.remove(loc1)
            keys_in_path.remove(loc2)
            if keys_in_path:
                continue
            elif doors_in_path:
                self.key2key_doors[tuple([loc1, loc2])] = ''.join(
                    sorted(doors_in_path))
            else:
                self.key_graph.add_edge(
                    loc1, loc2, weight=len(shortest_path) - 1)

class DoorState():
    def __init__(self, open_doors):
        self.open_doors = open_doors
        self.closed_doors
        self.accessible_keys = set()
        self.state_graph = nx.Graph()
        self.min_dist = np.inf
        self.min_loc = None


def initialize_vault(fn):
    vault = Vault()
    vault.input_to_map(fn)
    vault.build_key_graph()
    # # vault.get_key2key_distances('@')
    # vault.close_all_doors()

    return vault


fn = '18_test4.txt'
v = initialize_vault(fn)
print(v.key2key_doors)
