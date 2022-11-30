from collections import defaultdict
import numpy as np


def load_input(fn, bdict, h=None):
    if not h:
        with open(fn) as fh:
            h = fh.read().rstrip()

    b = ''.join([bdict[hx] for hx in h])
        
    return b


def get_b_dict(fn):
    bd = {}
    with open(fn) as fh:
        for l in fh.readlines():
            x, y = l.rstrip().split(' = ')
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
        sps = b[ind: ind + sp_len]
        print(sps)        
        return 'len', ind_end, ind
    
    elif b[ind] == '1':
        ind += 1
        spn = int(b[ind: ind + 11], 2)
        ind += 11
        
        return 'num', spn, ind


def parse_packet(ind, b):
    v, tp, ind = get_packet_info(ind, b)

    if tp==4:
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
    ind = 0
    versions = []
    version = 0
    level = 0
    lnum = defaultdict(int)
    llen = defaultdict(int)
    lop = defaultdict(int)
    lvals = defaultdict(list)
    ltype = defaultdict(str)
    out_str = ''
    
    end = False
    # for _ in range(5):
    while not end:
        try:
            ind, version, val, valtype, tp = parse_packet(ind, b)
        except:
            end = True
            break
        
        versions.append(version)
        level_tabs = ''.join(['\t' for x in range(level)])
        if valtype == 'literal':
            out_str += f'{level_tabs}{tp}\t{val}\n'
        else:
            out_str += f'{level_tabs}{tp}\n'

        print(f'ind:\t{ind}')
        print(f'level:\t{level}')
        print(f'type:\t{tp}')
        print(f'vtype:\t{valtype}')
        print(f'value:\t{val}')
        print(f'{level_tabs}{tp}, {val}\n')

        # Adjust current level based on valtype
        if valtype == 'num':
            level += 1
            lop[level] = tp
            # level += 1
            ltype[level] = valtype
            lnum[level] = int(val)
            # level += 1
            

        elif valtype == 'len':
            level += 1
            lop[level] = tp
            # level += 1
            ltype[level] = valtype
            llen[level] = int(val)
            # level += 1

        elif valtype == 'literal':
            # If literal value, append to list of values at this level
            lvals[level].append(val)

        if ltype[level] == 'num':
            if lnum[level] == 0:
                print('END num subs')
                print(lop[level], lvals[level])
                val = op_ans(lop[level], lvals[level])
                lvals[level] = []
                level -= 1
                lvals[level].append(val)

            else:
                lnum[level] -= 1

        if ltype[level] == 'len':
            if ind >= llen[level]:
                print('END len subs')
                print(lop[level], lvals[level])
                val = op_ans(lop[level], lvals[level])
                lvals[level] = []
                level -= 1
                lvals[level].append(val)    

        
        print(f'vals:\t{lvals}')
        print(f'types:\t{ltype}')
        print(f'ops:\t{lop}')
        print(f'nums:\t{lnum}')
        print(f'lens:\t{llen}')
        print()
    with open('out_str.txt', 'w') as fh:
        fh.write(out_str)
    # print(out_str)
    print(op_ans(lop[0], lvals[0]))
    return versions, lvals, lop


fn = '16.txt'
bdict = get_b_dict('b_dict.txt')
b = load_input(fn, bdict)

b = load_input(fn, bdict, '9C005AC2F8F0')

# parse_packet(0, '00111000000000000110111101000101001010010001001000000000')

versions, lvals, lop = run_program(b)
print(sum(versions))
# print(lvals)
# print(lop)

with open('out_list.txt', 'w') as fh:
    for l in np.arange(35, 0, -1):
        fh.write(f'level\t{l}\n')
        fh.write(f'op\t{lop[l]}\n')
        fh.write('\t')
        fh.write('\t'.join([str(x) for x in lvals[l]]))
        fh.write('\n\n')
    


