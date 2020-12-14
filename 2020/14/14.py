import re
from itertools import product
from collections import Counter


def read_lines(fn):
    lines = [g for g in open(fn).read().split('\n')]
    return lines


def step1(line, bitmask, mem):
    if 'mask' in line:
        bitmask = line[7:]
        return bitmask, mem
    else:
        mem_ind = int(re.search(r'mem\[(\d+)\]', line).group(1))
        mem_val = '{0:b}'.format(int(line.split(' = ')[1])).zfill(36)
        write_mem = ''
        for m, v in zip(bitmask, mem_val):
            if m == 'X':
                write_mem += v
            else:
                write_mem += m
        mem[mem_ind] = int(write_mem, 2)
        return bitmask, mem


def gen_masked_inds(mem_ind, bitmask):
    inds = ''
    for m, v in zip(bitmask, mem_ind):
        if m in '1X':
            inds += m
        elif m == '0':
            inds += v
    n_x = Counter(bitmask)['X']
    inds = inds.replace('X', '{}')
    for x in product('01', repeat=n_x):
        yield inds.format(*x)


def step2(line, bitmask, mem):
    if 'mask' in line:
        bitmask = line[7:]
        return bitmask, mem
    else:
        mem_ind = re.search(r'mem\[(\d+)\]', line).group(1)
        mem_ind = '{0:b}'.format(int(mem_ind)).zfill(36)
        mem_val = int(line.split(' = ')[1])

        for write_ind in gen_masked_inds(mem_ind, bitmask):
            mem[int(write_ind, 2)] = mem_val
        return bitmask, mem


def run_program(lines, part=1):
    mem = {}
    bitmask = ''.join(['X' for _ in range(36)])
    part_funcs = {1: step1, 2: step2}
    step = part_funcs[part]
    for line in lines:
        bitmask, mem = step(line, bitmask, mem)
    return sum([val for val in mem.values()])


# Part 1
lines = read_lines('14.txt')
print(f"Part 1:\t{run_program(lines, 1)}")
# Part 2
lines = read_lines('14.txt')
print(f"Part 2:\t{run_program(lines, 2)}")
