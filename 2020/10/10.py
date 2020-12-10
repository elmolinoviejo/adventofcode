from collections import Counter
import math


def get_nums(fn):
    nums = [int(line) for line in open(fn).read().split('\n')]
    return nums


def get_deltas(nums):
    j = 0
    deltas = []
    for a in sorted(nums):
        if a < j + 4:
            deltas.append(a - j)
            j = a
        else:
            return deltas
    return deltas


def count_sequential(deltas):
    seqs = {}
    count = 1
    for ind in range(len(deltas) - 1):
        if deltas[ind] == deltas[ind + 1]:
            count += 1
        else:
            if deltas[ind] in seqs:
                seqs[deltas[ind]].append(count)
            else:
                seqs[deltas[ind]] = [count]
            count = 1
    seqs[deltas[-1]].append(count)
    return seqs


def all_comb(n):
    # all combinations nCr where r is [len(n)...0]
    ac = 0
    for x in range(n + 1):
        ac += math.comb(n, x)
    return ac


def ways_from_seq(seqs):
    ans = 1
    for n in seqs[1]:
        m = all_comb(n - 1)
        if n > 3:
            m = m - 3**(n - 4)
        ans *= m
    return ans


nums = get_nums('10.txt')
deltas = get_deltas(nums)

# Part A
ans1 = (Counter(deltas)[1] * (Counter(deltas)[3] + 1))
print(f"Part A:\t{ans1}")

# Part B
seqs = count_sequential(deltas)
ans2 = ways_from_seq(seqs)
print(f"Part B:\t{ans2}")
