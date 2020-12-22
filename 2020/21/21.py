import re


def load_foods(fn):
    lines = [g for g in open(fn).read().split('\n')]
    foods = {}
    for fnum, line in enumerate(lines):
        line = line.replace(',', '')
        ing_list = re.search(r'^(.*) \(', line).group(1).split(' ')
        alrgn_list = re.search(r'contains (.*)\)', line).group(1).split(' ')
        foods[fnum] = (ing_list, alrgn_list)
    return foods


def get_possibilities(foods):
    alrgn_ings = {}
    for ings, alrgns in foods.values():
        for a in alrgns:
            if a not in alrgn_ings:
                alrgn_ings[a] = []
            alrgn_ings[a].append(ings)

    alrgn_possibilites = {}
    for a, ings_list in alrgn_ings.items():
        alrgn_possibilites[a] = set.intersection(*[set(i) for i in ings_list])

    return alrgn_possibilites


def match_ings(alrgn_possibilites):
    matched_ings = {}
    while len(matched_ings) < len(alrgn_possibilites):
        for alrgn, ings in alrgn_possibilites.items():
            if len(ings) == 1:
                matched_ings[alrgn] = list(ings)[0]
            for matched_ing in matched_ings.values():
                if matched_ing in ings:
                    alrgn_possibilites[alrgn].remove(matched_ing)
    return matched_ings


foods = load_foods('21.txt')
alrgn_possibilites = get_possibilities(foods)

all_possible = set()
[all_possible.union(i) for a, i in alrgn_possibilites.items()]

ans = 0
for ings, alrgns in foods.values():
    for i in ings:
        if i not in all_possible:
            ans += 1
print(f"Part 1:\t{ans}")

matched_ings = match_ings(alrgn_possibilites)
sorted_ings = {a: matched_ings[a] for a in sorted(matched_ings)}
print(f"Part 2:\t{','.join([i for i in sorted_ings.values()])}")
