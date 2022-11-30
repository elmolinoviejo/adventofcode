from itertools import combinations, product
import math

import networkx as nx
import numpy as np


def load_file(fn):
    snbs = {}
    with open(fn) as fh:
        scanners = fh.read().split('\n\n')
        for scanner in scanners:
            for ind, line in enumerate(scanner.split('\n')):
                if ind == 0:
                    # print(line)
                    sn = line.replace('-', '').rstrip().split('scanner ')
                    sn = int(sn[1])
                    snbs[sn] = []
                else:
                    snbs[sn].append(tuple([int(x) for x in line.split(',')]))
    return snbs


def get_vectors(bs):
    vectors = {}
    for ind1, ind2 in combinations(range(len(bs)), 2):
        b1 = bs[ind1]
        b2 = bs[ind2]
        v = tuple(x - y for x, y in zip(b1, b2))
        vectors[v] = (ind1, ind2)
    return vectors


def gen_rot_vectors():
    rot_vectors = {}
    pi = math.pi
    cos = np.cos
    sin = np.sin

    ind = 0
    for tx in [0, pi / 2, pi, -pi / 2]:
        rotx = np.array([[1, 0, 0],
                        [0, cos(tx), -1 * sin(tx)],
                        [0, sin(tx), cos(tx)]])
        for ty, tz in ([0, 0],
                       [0, pi / 2],
                       [0, pi],
                       [0, -pi / 2],
                       [pi / 2, pi / 2],
                       [-pi / 2, -pi / 2]):

            roty = np.array([[cos(ty), 0, sin(ty)],
                             [0, 1, 0],
                             [-1 * sin(ty), 0, cos(ty)]])

            rotz = np.array([[cos(tz), -1 * sin(tz), 0],
                             [sin(tz), cos(tz), 0],
                             [0, 0, 1]])

            rot = rotz.dot(roty).dot(rotx)
            rot_vectors[ind] = np.around(rot, decimals=0)
            ind += 1
    return rot_vectors


# fix for vectors
def make_rot_sets(svectors, rvs):
    # make all rotations sets
    snv_rots = dict()
    for s, svs in svectors.items():
        snv_rots[s] = {}
        for rotind, rot in rvs.items():
            snv_rots[s][rotind] = set()
            for v in svs.keys():
                rv = tuple([int(x) for x in rot.dot(np.array(v))])
                snv_rots[s][rotind].add(rv)
    return snv_rots


def make_rot_lists(svectors, rvs):
    # make all rotations sets
    snv_rots = dict()
    for s, svs in svectors.items():
        snv_rots[s] = {}
        for rotind, rot in rvs.items():
            snv_rots[s][rotind] = {}
            for v, inds in svs.items():
                # rv = tuple([int(x) for x in rot.dot(np.array(v))])
                snv_rots[s][rotind][v] = inds
    return snv_rots


rvs = gen_rot_vectors()

fn = '19.txt'
fn = '19_test.txt'
snbs = load_file(fn)

svectors = dict()
for s, bs in snbs.items():
    svectors[s] = get_vectors(bs)

snv_rots = make_rot_lists(svectors, rvs)


# store scanner pairs (>= 11 vector matches)
# store rotation for second scanner
# store first vector that matches
G = nx.Graph() # nodes are scanners, edges are rotations with attr rotind
for s1, s2 in combinations(snbs.keys(), 2):
    svs1 = set(snv_rots[s1][0].keys())
    for rotind, svs2_dict in snv_rots[s2].items():
        svs2 = set(svs2_dict.keys())
        matches = svs1 & svs2
        nmatch = len(matches)
        print(s1, s2, rotind, nmatch)
        if nmatch > 11:
            G.add_edge(s1, s2, rotind=rotind, mv=matches.pop())

rot_dict = dict()
rot_dict[0] = []

for s2 in G:
    if s2 == 0:
        continue
    rot_dict[s2] = []
    sp = nx.shortest_path(G, 0, s2)
    for e in zip(sp, sp[1:]):
        rot_dict[s2].append(G.get_edge_data(*e)['rotind'])

rot_snbs = {}
for s, rots in rot_dict.items():
    rot_snbs[s] = []
    rotv = rvs[0]
    while len(rots) > 0:
        rind = rots.pop()
        rotv = rotv.dot(np.linalg.inv(rvs[rind]))
    for b in snbs[s]:
        rot_snbs[s].append(tuple([
            int(x) for x in rotv.dot(b)]))

# # recalc vectors
# svectors = dict()
# for s, bs in snbs.items():
#     svectors[s] = get_vectors(bs)
# # print(svectors[0])
# print(rot_dict)
# # for s, bs in rot_snbs.items():
# #     print(s)
# #     [print(b) for b in bs]
# #     print()


# still need translations
