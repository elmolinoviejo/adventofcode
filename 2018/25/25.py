from itertools import product


def load_points(fn):
    points = set()
    for line in open(fn).readlines():
        point = tuple([int(x) for x in line.rstrip().split(',')])
        points.add(point)
    return points


points = load_points('25.txt')
# points = load_points('25test.txt')

diffs = [tuple(x) for x in product((-3, -2, -1, 0, 1, 2, 3), repeat=4)]
diffs = [d for d in diffs if sum([abs(d[0]),
                                  abs(d[1]),
                                  abs(d[2]),
                                  abs(d[3])]) < 4]
diffs = list(set(diffs))

const = []
ind = 0
while len(points) > 0:
    p = points.pop()
    const.append([])
    const[ind].append(p)
    p_to_check = [p]
    while len(p_to_check) > 0:
        current_loc = p_to_check.pop()
        for diff in diffs:
            adj = tuple([x + d for x, d in zip(current_loc, diff)])
            if adj in points:
                const[ind].append(adj)
                points.remove(adj)
                p_to_check.append(adj)
    ind += 1

print(f"Part 1:\t{len(const)}")
