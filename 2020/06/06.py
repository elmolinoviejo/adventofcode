def input_to_groups(fn):
    groups = [g.split('\n') for g in open(fn).read().split('\n\n')]
    return groups


def solve_groups(groups):
    na, nb = 0, 0
    for group in groups:
        sets = [set(g) for g in group]
        na += len(set.union(*sets))
        nb += len(set.intersection(*sets))
    print(f"Part 1:\t{na}")
    print(f"Part 2:\t{nb}")


solve_groups(input_to_groups('06.txt'))
