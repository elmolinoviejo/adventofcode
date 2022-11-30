from collections import deque
from itertools import product
from math import ceil, floor
import re


def explode_check(sn):
    ns = [str(x) for x in range(10)]
    pattern = '[\[,]*([0-9]+)[\],]'
    exppattern = '[0-9]+,[0-9]+'

    exp = False
    lvl = 0
    ind_ns = {}
    elind, erind = None, None
    skipind = set()
    for ind, s in enumerate(sn):
        if ind in skipind:
            continue
        if s == '[':
            lvl += 1
        elif s == ']':
            lvl -= 1
        elif s in ns:
            num = re.search(pattern, sn[ind:])
            num = int(num.group(1))
            skipind.update([x for x in range(ind, ind + len(str(num)))])
            ind_ns[ind] = num

            if lvl > 4 and not exp:
                exp = True
                pair = re.search(exppattern, sn[ind:])
                pair = pair.group(0)
                explval, exprval = [int(x) for x in pair.split(',')]
                ind_ns[ind + len(str(explval)) + 1] = exprval

                elind = ind
                erind = ind + len(pair)
                skipind.update([x for x in range(elind, erind + 1)])
    return exp


def explode_sn(sn):
    ns = [str(x) for x in range(10)]
    pattern = '[\[,]*([0-9]+)[\],]'
    exppattern = '[0-9]+,[0-9]+'

    exp = False
    lvl = 0
    ind_ns = {}
    elind, erind = None, None
    skipind = set()
    for ind, s in enumerate(sn):
        if ind in skipind:
            continue
        if s == '[':
            lvl += 1
        elif s == ']':
            lvl -= 1
        elif s in ns:
            num = re.search(pattern, sn[ind:])
            num = int(num.group(1))
            skipind.update([x for x in range(ind, ind + len(str(num)))])
            ind_ns[ind] = num

            if lvl > 4 and not exp:
                exp = True
                pair = re.search(exppattern, sn[ind:])
                pair = pair.group(0)
                explval, exprval = [int(x) for x in pair.split(',')]

                elind = ind
                erind = ind + len(str(explval)) + 1
                ind_ns[erind] = exprval
                skipind.update(range(elind, erind + len(str(exprval))))

    # print(ind_ns)

    if not exp:
        return sn

    # Check left
    lind, lval = None, None
    for ind in reversed(range(elind)):
        if ind in ind_ns:
            lind = ind
            lval = int(ind_ns[ind])
            break

    # Check right
    rind, rval = None, None
    for ind in range(erind + 1, len(sn) + 1):
        if ind in ind_ns:
            rind = ind
            rval = int(ind_ns[ind])
            break

    # print(f'explode:{explval, exprval}') 
    # print(f'explodei:{elind, erind}') 
    # print(f'left:\t{lind, lval}')
    # print(f'right:\t{rind, rval}')
    new_sn = ''


    # Rewrite this logic to account for larger numbers
    skipwrite = set()
    if lval:
        skipwrite.update(range(lind + 1, lind + len(str(lval))))
    # else:
    #     continue
    if rval:
        skipwrite.update(range(rind + 1, rind + len(str(rval))))
    # else:
    #     continue
    # skipwrite.add(elind - 1)
    # skipwrite.add(elind - 1)
    skipwrite.add(erind - 1)
    # skipwrite.update(range(elind + 1, elind + len(str(explval))))
    # skipwrite.update(range(erind + 1, erind + len(str(exprval))))
    skipwrite.update(range(elind, erind + len(str(exprval)) + 1))

    # skipind.update(range(elind - 1, erind + 1))

    for ind, s in enumerate(sn):
        if ind in skipwrite:
            continue

        elif ind == lind:
            new_val = str(lval + explval)
            new_sn += new_val

        # elif ind == elind and lind == None:
        #     new_sn += '0'

        # elif ind == elind and lind and rind:
        #     new_sn += '0'

        # elif ind == erind and rind == None:
        #     new_sn += '0'
        elif ind == elind - 1:
            new_sn += '0'

        elif ind == erind and lind and rind:
            continue

        elif ind == rind:
            new_val = str(rval + exprval)
            new_sn += new_val

        else:
            # print(ind, s)
            new_sn += s
    #     print(ind, new_sn)
    # print(skipwrite)        

    return new_sn


def split_check(sn):
    spl = False
    pattern = '[\[,]([0-9]{2,})[\],]'
    ms = re.finditer(pattern, sn)

    if len(tuple(ms)) == 0:
        return False
    else:
        return True


def split_sn(sn):
    # spl = False
    pattern = '[\[,]([0-9]{2,})[\],]'
    # ms = finditer(pattern, sn)

    # if len(tuple(ms)) == 0:
    #     return sn, spl

    ms = re.finditer(pattern, sn)
    for m in ms:
        spl = True
        sval = int(m.group(1))
        # print(m.group(1))
        sinds = m.span(1)
        # print(sval, sinds)
        break

    new_sn = ''
    for ind, s in enumerate(sn):
        if ind == sinds[0]:
            lval = int(floor(sval / 2))
            rval = int(ceil(sval / 2))
            new_sn += f'[{lval},{rval}]'
        if ind in range(sinds[0], sinds[1]):
            continue
        else:
            new_sn += s
    return new_sn


def add_sn(sn1, sn2):
    return f'[{sn1},{sn2}]'


def reduce_sn(sn, verbose=False):
    done = False
    while not done:
        if explode_check(sn):
            sn = explode_sn(sn)
            if verbose:
                print('explode')
                print(sn)
            continue
        if split_check(sn):
            sn = split_sn(sn)
            if verbose:
                print('split')
                print(sn)
            continue
        if explode_check(sn) or split_check(sn):
            continue
        else:
            return sn


def solve_hw(fn):
    with open(fn) as fh:
        sns = fh.read().split('\n')
    sns.reverse()

    while len(sns) > 1:
        sn1 = sns.pop()
        sn2 = sns.pop()
        sn_sum = add_sn(sn1, sn2)
        # print(sn_sum)
        sn = reduce_sn(sn_sum, False)
        # print(sn_sum)
        sns.append(sn)
    return sn


def get_score(sn):
    pattern = '\[([0-9]+,[0-9]+)\]'
    match = re.search(pattern, sn)
    while match:
        # match = re.search(pattern, sn)
        nums = [int(x) for x in match.group(1).split(',')]
        mag = nums[0] * 3 + nums[1] * 2
        span = match.span()
        # print(nums, span)

        sn_new = ''
        for ind, s in enumerate(sn):
            if ind == span[0]:
                sn_new += str(mag)
            elif ind in range(span[0] + 1, span[1]):
                continue
            else:
                sn_new += s
        sn = sn_new
        # print(sn)
        match = re.search(pattern, sn)
    return sn


fn = '18.txt'
# sn = solve_hw(fn)
# score = get_score(sn)
# print(score)

with open(fn) as fh:
    sns = fh.read().split('\n')

maxmag = 0
for i1, i2 in product(range(len(sns)), range(len(sns))):
    if i1 == i2:
        continue
    sn1 = sns[i1]
    sn2 = sns[i2]
    sn = add_sn(sn1, sn2)
    sn = reduce_sn(sn)
    mag = int(get_score(sn))
    if mag > maxmag:
        maxmag = mag
        max_sn = [sn1, sn2]

print(max_sn[0])
print(max_sn[1])
print(maxmag)
