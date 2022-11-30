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
        v = tuple(y - x for x, y in zip(b1, b2))
        # vectors[(ind1, ind2)] = v
        vectors[v] = (ind1, ind2)
    return vectors


def gen_rot_vectors():
    rot_vectors = {}
    pi = math.pi
    cos = np.cos
    sin = np.sin

    ind = 0
    for tx in [0, pi/2, pi, -pi/2]:
        rotx = np.array([[1, 0, 0],
                       [0, cos(tx), -1 * sin(tx)],
                       [0, sin(tx), cos(tx)]])
        for ty, tz in ([0, 0],
                       [0, pi/2],
                       [0, pi],
                       [0, -pi/2],
                       [pi/2, pi/2],
                       [-pi/2, -pi/2]):

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


rvs = gen_rot_vectors()

fn = '19.txt'
# fn = '19_test.txt'
snbs = load_file(fn)

# #simple test
# snbs = {0:[], 1:[], 2:[]}
# for x in range(13):
#     snbs[0].append(tuple([x, 1, 1]))
#     snbs[1].append(tuple([x+15, -1, 1]))
#     snbs[2].append(tuple([x-15, 1, 0]))
# snbs[0] = [(1, 0, 0), (2, 0, 0)]
# snbs[1] = [(2, 0, 0), (3, 0, 0), (3, 5, 2)]


# snbs = {k:v for k, v in snbs.items() if k < 2}

svectors = dict() # svectors[scanner][vector] = (b1, b2)
for s, bs in snbs.items():
    svectors[s] = get_vectors(bs)

snv_rots = make_rot_sets(svectors, rvs)

# print(0)
# [print(k) for k, v in svectors[0].items() if v==(0, 1)]
# print()
# print(1)
# [print(k) for k, v in svectors[1].items() if v==(3, 8)]


G = nx.DiGraph() # nodes are scanners, edges are rotations with attr rotind

for s1, s2 in combinations(snbs.keys(), 2):
    svs1 = snv_rots[s1][0]
    for rotind, svs2 in snv_rots[s2].items():
        matches = svs1 & svs2
        nmatch = len(matches)
        if nmatch > 11:
            # find translations
            match = matches.pop()
            vm1 = svectors[s1][match][0]
            vm2 = svectors[s2][tuple([int(x) for x in 
                    np.linalg.inv(rvs[rotind]).dot(np.array(match))])][0]

            m1 = snbs[s1][vm1]
            m2 = tuple([int(x) for x in 
                    rvs[rotind].dot(snbs[s2][vm2])])

            trans = [int(x) for x in (a - b for a, b in zip(m1, m2))]

            # print(s1, s2, rotind, trans)

            G.add_edge(s1, s2, rotind=rotind, trans=trans, inv=False)
            break

for n1, n2, att in G.edges(data=True):
    if (n2, n1) not in G.edges:
        G.add_edge(n2, n1,
            rotind=att['rotind'],
            trans=att['trans'],
            inv=True)


tx_order = dict()
tx_order[0] = []

for s2 in G:
    if s2 == 0:
        continue
    tx_order[s2] = [] 
    sp = nx.shortest_path(G, 0, s2)
    for e in zip(sp, sp[1:]):
        tx_order[s2].append(tuple([
            G.get_edge_data(*e)['rotind'],
            G.get_edge_data(*e)['trans'],
            G.get_edge_data(*e)['inv']]))

# print(tx_order)

# rot_dict = {0: []}
# sn_final_rots = {0: rvs[0]}

# print(snbs[1][0])
trans_locs = []
tx_snbs = {}
for s, txs in tx_order.items():
    tl = [0, 0, 0]
    bs = [x for x in snbs[s]]
    while len(txs) > 0:
        rind, trans, inv = txs.pop()
        # print()
        # print(s, rind, trans, inv)
        # print('-----------------')
        rotv = rvs[rind]
        newbs = []
        '''
        3: -(2) + (1)
        2:  (3) - (2) + (1)
        '''
        if inv:
            rotv = np.linalg.inv(rvs[rind])
            tl = [a - t for a, t in zip(tl, trans)]
            tl = rotv.dot(tl)
        else:
            tl = rotv.dot(tl)
            tl = [t + a for a, t in zip(tl, trans)]

        for b in bs:
            # print(b)
            if inv:
                rotv = np.linalg.inv(rvs[rind])
                b = [a - t for a, t in zip(b, trans)]
                b = rotv.dot(b)
            else:
                b = rotv.dot(b)
                b = [t + a for a, t in zip(b, trans)]

            newbs.append(tuple([int(x) for x in b]))
            bs = [x for x in newbs]
    trans_locs.append(list(tl))
    tx_snbs[s] = bs

# final_bs = set()
# for s, bs in tx_snbs.items():
#     final_bs.update(bs)
#     print(len(final_bs))
#     # print(s)
#     # [print(b) for b in bs]
#     # print()

# trans_locs = []
# print(trans_locs)
# [print(t) for t in trans_locs]
maxdist = 0
for t1, t2 in combinations(trans_locs, 2):
    # print(t1, t2)
    dist = sum(abs(x-y) for x, y in zip(t1, t2))
    if dist > maxdist:
        maxdist = dist
print(maxdist)

#10899 too low

# # print(len(final_bs))
# x = [x for x in final_bs]
# x.sort()
# with open('19_out.txt', 'w') as fh:
#     for s, bs in tx_snbs.items():
#         fh.write(str(s))
#         fh.write('\n')
#         for b in bs:
#             fh.write(str(b))
#             fh.write('\n')
#         fh.write('\n\n')



# still need translations
