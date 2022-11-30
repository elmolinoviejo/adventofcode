import numpy as np

import networkx as nx


def load_input(fn, bdict, h=None):
    if not h:
        with open(fn) as fh:
            h = fh.read().rstrip()

    b = ''.join([bdict[hx] for hx in h])

    return b


def get_b_dict(fn):
    bd = {}
    with open(fn) as fh:
        for line in fh.readlines():
            x, y = line.rstrip().split(' = ')
            bd[x] = y
    return bd


def get_packet_info(ind, b):
    version = int(b[ind:ind + 3], 2)
    ind += 3
    tp = int(b[ind:ind + 3], 2)
    ind += 3
    return version, tp, ind


def ptype4(ind, b):
    end = False
    packets = []
    while not end:
        p = b[ind: ind + 5]
        packets.append(p)
        ind += 5
        if p[0] == '0':
            end = True

    bval = ''
    for p in packets:
        bval += p[1:]
    val = int(bval, 2)
    return 'literal', val, ind


def ptype(ind, b):
    if b[ind] == '0':
        ind += 1
        sp_len = int(b[ind:ind + 15], 2)
        ind += 15
        ind_end = sp_len + ind
        # sps = b[ind: ind + sp_len]
        # print(sps)
        return 'len', ind_end, ind

    elif b[ind] == '1':
        ind += 1
        spn = int(b[ind: ind + 11], 2)
        ind += 11

        return 'num', spn, ind


def parse_packet(ind, b):
    v, tp, ind = get_packet_info(ind, b)

    if tp == 4:
        valtype, val, ind = ptype4(ind, b)
        return ind, v, val, valtype, tp
    else:
        valtype, val, ind = ptype(ind, b)
        return ind, v, val, valtype, tp


def op_ans(tn, vals):
    tn = int(tn)
    if tn == 0:
        return sum(vals)
    if tn == 1:
        return np.prod(vals)
    if tn == 2:
        return min(vals)
    if tn == 3:
        return max(vals)
    if tn == 5:
        if vals[0] > vals[1]:
            return 1
        else:
            return 0
    if tn == 6:
        if vals[0] < vals[1]:
            return 1
        else:
            return 0
    if tn == 7:
        if vals[0] == vals[1]:
            return 1
        else:
            return 0


def run_program(b):
    G = nx.DiGraph()
    ind = 0
    parent = 0
    end = False
    # for _ in range(10):
    while not end:
        try:
            endind, version, val, valtype, tpid = parse_packet(ind, b)
        except:
            end = True
            break

        # find parent for this new node
        if parent:
            # continue to go up levels until find an incomplete parent
            complete = True
            while complete:
                # Check if parent node is complete
                pvt = G.nodes[parent]['valtype']
                pv = G.nodes[parent]['val']

                if pvt == 'num':
                    if pv == 0:
                        # parent complete, move parent to next level up
                        parent = G.nodes[parent]['parent']
                        complete = True
                    else:
                        # parent incomplete, keep same parent
                        G.nodes[parent]['val'] -= 1
                        complete = False

                elif pvt == 'len':
                    if endind > pv:
                        parent = G.nodes[parent]['parent']
                        complete = True
                    else:
                        complete = False
        else:
            parent = 0

        G.add_node(ind,
                   valtype=valtype,
                   val=val,
                   val0=val,
                   tpid=tpid,
                   parent=parent
                   )
        # G.nodes[ind]['parent'] = parent

        G.add_edge(parent, ind)

        if tpid != 4:
            parent = ind
        ind = endind

    G.remove_edge(0, 0)
    return G


def solve(G):
    complete_nodes = set()
    while len(complete_nodes) < G.number_of_nodes():
        for n in G:
            if n in complete_nodes:
                continue
            complete = True
            vals = []
            # print(n)
            for sn in G.adj[n]:
                vals.append(G.nodes[sn]['val'])
                tpid = G.nodes[sn]['tpid']
                if tpid == 4:
                    complete_nodes.add(sn)
                else:
                    complete = False
            if complete:
                G.nodes[n]['val'] = op_ans(G.nodes[n]['tpid'], vals)
                G.nodes[n]['tpid'] = 4
                complete_nodes.add(n)
    return G.nodes[0]['val'], G


fn = '16.txt'
bdict = get_b_dict('b_dict.txt')

b = load_input(fn, bdict)
G = run_program(b)
ans, G = solve(G)
print(ans)
