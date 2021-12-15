from collections import Counter, deque


def load_input(fn):
    with open(fn) as fh:
        temp, _, *pis = fh.read().split('\n')
        pis = dict([x.split(' -> ') for x in pis])
    return temp, pis


def step(tc, pc, pis):
    for p, c in tc.copy().items():
        p1, p2 = p
        mid = pis[p]
        tc[p] -= c
        tc[p1 + mid] += c
        tc[mid + p2] += c
        pc[mid] += c
    return tc, pc


def get_ans(pc):
    return pc.most_common()[0][1] - pc.most_common()[-1][1]


fn = '14.txt'
temp, pis = load_input(fn)

tc = Counter()
pc = Counter(temp)
for p1, p2 in zip(temp, temp[1:]):
    tc[p1 + p2] += 1

for s in range(40):
    tc, pc = step(tc, pc, pis)
    if s == 9:
        print(get_ans(pc))
print(get_ans(pc))
