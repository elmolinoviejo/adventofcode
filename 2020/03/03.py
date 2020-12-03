import numpy as np


def input_to_tree_map(fn):
    tree_map = []
    with open(fn) as fh:
        for line in fh.readlines():
            tree_map.append(line.rstrip())
    return tree_map


def tree_count(slope, tree_map):
    n_trees = 0
    row, col = 0, 0
    width = len(tree_map[0])
    while True:
        col = (col + slope[0]) % width
        row += slope[1]
        if row >= len(tree_map):
            break
        if tree_map[row][col] == '#':
            n_trees += 1
    return n_trees


tree_map = input_to_tree_map('03.txt')

# Part 1
print('Part 1:')
print(tree_count((3, 1), tree_map))
# Part 2
print('Part 2:')
slopes = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
prod = 1
for slope in slopes:
    prod = prod * tree_count(slope, tree_map)
print(prod)
