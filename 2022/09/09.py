def read_input(fn):
    moves = []
    with open(fn) as fh:
        for m in fh.readlines():
            m1, m2 = m.rstrip().split()
            moves.append(tuple([m1, int(m2)]))
    return moves

def sign(num):
    if num < 0:
        return -1
    elif num > 0:
        return 1
    else:
        return 0


def move_knot(hloc, kloc):
    x1, y1 = hloc
    x2, y2 = kloc

    dx = x1 - x2
    dy = y1 - y2

    if abs(dx) < 2 and abs(dy) < 2:
        return kloc
    else:
        return(tuple([x2 + sign(dx), y2 + sign(dy)]))


def move_rope(m, klocs):
    dms = {
        'U': (0, -1),
        'D': (0, 1),
        'L': (-1, 0),
        'R': (1, 0)
        }

    d, dist = m
    dx, dy = dms[d]
    visited = set()
    for _ in range(dist):
        hloc = klocs[0]
        x, y = hloc
        hloc = tuple([x + 1 * sign(dx),
                      y + 1 * sign(dy)])
        klocs[0] = hloc
        for ind in range(len(klocs)):
            if ind == 0:
                continue
            hloc = klocs[ind - 1]
            kloc = klocs[ind]
            kloc = move_knot(hloc, kloc)
            klocs[ind] = kloc
            if ind == len(klocs) - 1:
                visited.add(klocs[-1])
        # print(klocs)
    return klocs, visited


moves = read_input('09.txt')

print('Part 1')
klocs = [tuple([0, 0]) for _ in range(2)]
all_klocs = set()
for m in moves:
    klocs, visited = move_rope(m, klocs)
    all_klocs.update(visited)
print(len(all_klocs))

print('Part 2')
klocs = [tuple([0, 0]) for _ in range(10)]
all_klocs = set()
for m in moves:
    klocs, visited = move_rope(m, klocs)
    all_klocs.update(visited)
print(len(all_klocs))




