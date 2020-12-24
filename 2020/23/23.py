def init_neighbors(cups):
    n = dict()  # dictionary of next cups
    for ind, c in enumerate(cups):
        if ind == len(cups) - 1:
            n[c] = cups[0]
        else:
            n[c] = cups[ind + 1]
    return n


def round(n, c0, minc=1, maxc=9):
    pick = [c0]
    for _ in range(3):
        pick.append(n[pick[-1]])
    pick.remove(c0)
    # print(pick)
    target = c0 - 1
    while True:
        if target < minc:
            target = maxc
        if target not in pick:
            break
        else:
            target -= 1

    # update neighbors
    n[c0] = n[pick[-1]]
    n[pick[-1]] = n[target]
    n[target] = pick[0]
    c0 = n[c0]

    return n, c0


# Part 1
cups = '487912365'
cups = [int(c) for c in cups]
n = init_neighbors(cups)
c0 = 4
for _ in range(100):
    n, c0 = round(n, c0)

ans = ''
c = 1
while True:
    c = n[c]
    ans += str(c)
    if c == 1:
        break
print(f"Part 1:\t{ans}")

# Part 2
cups = '487912365'
cups = [int(c) for c in cups]
n = init_neighbors(cups)
# add to 1000000
for c in range(1000001):
    if c in n:
        continue
    n[c] = c + 1
n[cups[-1]] = 10
n[1000000] = cups[0]

c0 = 4
for _ in range(10000000):
    n, c0 = round(n, c0, maxc=1000000)

ans = n[1] * n[n[1]]
print(f"Part 2:\t{ans}")
