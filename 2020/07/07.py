import re


def import_bag_pairs(fn):
    rules = [g for g in open(fn).read().split('\n')]

    inner_outer = {}
    outer_inner = {}
    for r in rules:
        re_matches = re.findall(r'((\d+)\s)?(\w+\s\w+)\sbag', r)
        for ind, match in enumerate(re_matches):
            if ind == 0:
                outer_bag = match[2]
                # if outer_bag == 'shiny gold':
                #     print(re_matches)
            else:
                inner_bag = match[2]
                if inner_bag == 'no other':
                    inner_bag_num = 0
                else:
                    inner_bag_num = int(match[1])

                if inner_bag not in inner_outer:
                    inner_outer[inner_bag] = [outer_bag]
                else:
                    inner_outer[inner_bag].append(outer_bag)

                if outer_bag not in outer_inner:
                    outer_inner[outer_bag] = [(inner_bag_num, inner_bag)]
                else:
                    outer_inner[outer_bag].append((inner_bag_num, inner_bag))
    return inner_outer, outer_inner


def num_containing_bags(inner_outer, start_bag):
    bags_checked = []
    bags_to_check = [start_bag]
    while len(bags_to_check) > 0:
        bag = bags_to_check.pop()
        if bag not in bags_checked:
            bags_checked.append(bag)
            if bag in inner_outer:
                bags_to_check.extend([b for b in inner_outer[bag]
                                      if b not in bags_checked])
    return len(bags_checked) - 1


def num_bags_within(outer_inner, start_bag):
    n_bags = -1
    bags_to_count = {start_bag: 1}
    while len(bags_to_count) > 0:
        bag = list(bags_to_count.keys()).pop()
        n_bag = bags_to_count.pop(bag)
        n_bags += n_bag
        if bag == 'no other':
            continue
        for next_num, next_bag in outer_inner[bag]:
            if next_bag in bags_to_count:
                bags_to_count[next_bag] += next_num * n_bag
            else:
                bags_to_count[next_bag] = next_num * n_bag
    return n_bags


inner_outer, outer_inner = import_bag_pairs('07.txt')
part1 = num_containing_bags(inner_outer, 'shiny gold')
part2 = num_bags_within(outer_inner, 'shiny gold')
print(f"Part A:\t{part1}\nPart B:\t{part2}")
