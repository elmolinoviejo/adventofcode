from itertools import product


def load_input(fn):
    '''
    Load reboot steps from file
    '''
    rbs = []
    with open(fn) as fh:
        for line in fh.read().split('\n'):
            status, coords = line.split(' ')
            x, y, z = coords.split(',')
            ds = []
            for d in [x, y, z]:
                ds.append(tuple(int(x) for x in d.split('=')[1].split('..')))
            rbs.append(tuple([status, tuple(ds)]))
    return rbs


def step_restrict(rb, onset):
    '''
    Perform reboot step with volume restriction
    '''
    status, ds = rb
    (x1, x2), (y1, y2), (z1, z2) = ds
    x1 = max(x1, -50)
    y1 = max(y1, -50)
    z1 = max(z1, -50)

    x2 = min(x2, 50)
    y2 = min(y2, 50)
    z2 = min(z2, 50)
    for loc in product(range(x1, x2 + 1),
                       range(y1, y2 + 1),
                       range(z1, z2 + 1)):
        if status == 'on':
            onset.add(loc)
        else:
            onset.discard(loc)
    return onset


def is_within(d1, d2):
    '''
    True if d1 is within d2
    '''
    (x1, x2), (y1, y2), (z1, z2) = d1
    (a1, a2), (b1, b2), (c1, c2) = d2

    for dim in range(3):
        if min(d1[dim]) < min(d2[dim]):
            return False
        if max(d1[dim]) > max(d2[dim]):
            return False
    return True


def calc_volume(d1):
    vol = 1
    for dim in d1:
        vol *= (max(dim) - min(dim)) + 1
    return vol


def check_overlap(d1, d2):
    (x1, x2), (y1, y2), (z1, z2) = d1
    (a1, a2), (b1, b2), (c1, c2) = d2

    n = ((min(a2, x2) - max(a1, x1) >= 0) and
         (min(b2, y2) - max(b1, y1) >= 0) and
         (min(c2, z2) - max(c1, z1) >= 0))

    return n


def split_overlap(d1, d2):
    (x1, x2), (y1, y2), (z1, z2) = d1
    (a1, a2), (b1, b2), (c1, c2) = d2

    locs = {}
    locs['x'] = (x1, x2, a1, a2)
    locs['y'] = (y1, y2, b1, b2)
    locs['z'] = (z1, z2, c1, c2)

    edges = dict()
    for dim in 'xyz':
        edges[dim] = []
        edges[dim].append(
            tuple(
                [min(locs[dim][0], locs[dim][2]),
                 max(locs[dim][0], locs[dim][2]) - 1]))

        edges[dim].append(
            tuple(
                [max(locs[dim][0], locs[dim][2]),
                 min(locs[dim][1], locs[dim][3])]))

        edges[dim].append(
            tuple(
                [min(locs[dim][1], locs[dim][3]) + 1,
                 max(locs[dim][1], locs[dim][3])]))

    cuboids = []
    for x, y, z in product(edges['x'], edges['y'], edges['z']):
        cuboids.append((x, y, z))
    # print(cuboids)

    overlaps = ([], [], [])
    for c in cuboids:
        in_d1 = is_within(c, d1)
        in_d2 = is_within(c, d2)
        if in_d1 and not in_d2:
            overlaps[0].append(c)
        if in_d2 and not in_d1:
            overlaps[1].append(c)
        if in_d1 and in_d2:
            overlaps[2].append(c)

    return overlaps  # 0: in d1 only, 1: in d2 only, 2: shared


def combine_steps(rbs, verbose=False):
    final_set = []  # list of all on cuboids
    while rbs:
        rbs_updated = []
        rb1 = rbs.pop()
        s1, d1 = rb1

        for rb2 in rbs.copy():
            s2, d2 = rb2

            if s1 == s2:
                rbs_updated.append(rb2)
                continue

            else:
                if check_overlap(d1, d2):
                    overlaps = split_overlap(d1, d2)
                    rbs_updated.extend([tuple([s2, o]) for o in overlaps[1]])

                else:
                    rbs_updated.append(rb2)
                    continue

        # Update rbs based on overlaps above
        rbs = rbs_updated

        if s1 == 'on':
            final_set.append(d1)
        if verbose:
            print(len(rbs))
    return final_set


def calc_final_set(final_set, verbose=False):
    ans = 0
    while final_set:
        d1 = final_set.pop()
        add_val = True
        for d2 in final_set.copy():
            if check_overlap(d1, d2):
                overlaps = split_overlap(d1, d2)
                add_val = False
                final_set.remove(d2)
                for os in overlaps:
                    final_set.extend([o for o in os])
                break
        if add_val:
            ans += calc_volume(d1)

        if verbose:
            print(len(final_set))
    return ans


fn = '22.txt'
# fn = '22_test.txt'
rbs = load_input(fn)

final_set = combine_steps(rbs, False)
# print(final_set)
print('final set complete')
print(sum([calc_volume(d) for d in final_set]))
ans = calc_final_set(final_set, True)
print(ans)



# rb1 = ('on', [(1, 1), (1, 1), (3, 10)])
# rb2 = ('on', [(0, 2), (0, 2), (0, 2)])

# print(check_overlap(rb1[1], rb2[1]))

test = False
if test:
    # get all cubiods
    # ---------------
    # within
    rb1 = ('on', [(1, 1), (1, 1), (1, 1)])
    rb2 = ('on', [(0, 2), (0, 2), (0, 2)])

    # # # one corner
    # rb1 = ('on', [(3, 4), (3, 4), (3, 4)])
    # rb2 = ('on', [(0, 3), (0, 3), (0, 3)])

    # # one edge
    # rb1 = ('on', [(0, 3), (3, 5), (3, 5)])
    # rb2 = ('on', [(0, 3), (0, 3), (0, 3)])

    # # none
    # rb1 = ('on', [(4, 5), (4, 5), (4, 5)])
    # rb2 = ('on', [(0, 3), (0, 3), (0, 3)])

    # # # identical
    # rb1 = ('on', ((0, 1), (0, 1), (0, 1)))
    # rb2 = ('off', ((0, 1), (0, 1), (0, 1)))


    overlaps = split_overlap(rb1[1], rb2[1])
    print(len(overlaps[0]), len(overlaps[1]), len(overlaps[2]))
    print(calc_volume(rb1[1]),
          calc_volume(rb2[1]),
          calc_volume(rb1[1]) + calc_volume(rb2[1]))
    area_sum = 0
    for o in overlaps:
        for c in o:
            area_sum += calc_volume(c)
            print(f'{c}\t{calc_volume(c)}')
        print('\n')
    print(f'Sum:\t{area_sum}')
