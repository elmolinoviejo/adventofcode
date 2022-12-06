from re import findall
from collections import deque


def read_input(fn, ncols):
    with open(fn, 'r') as fh:
        crates, steps = fh.read().split('\n\n')

    crates = crates.split('\n')
    steps = steps.split('\n')

    stacks = [deque() for x in range(ncols)]
    for crate_line in crates[:-1]:
        for c in range(ncols):
            ind = (c * 4) + 1
            lett = crate_line[ind]
            if lett!=' ':
                stacks[c].append(lett)
                

    moves = []
    for line in steps:
        move_nums = findall(r'\d+', line)
        moves.append(tuple([int(x) for x in move_nums]))

    return stacks, moves


def move_crates(move, stacks, how='one'):
    '''
    how = 'one' or 'all'
    '''
    n_moves, fr, to = move
    queue = deque()
    for _ in range(n_moves):
        lett = stacks[fr - 1].popleft()
        queue.appendleft(lett)
    if how=='one':
        while queue:
            stacks[to - 1].appendleft(queue.pop())
    elif how=='all':
        stacks[to - 1].extendleft(queue)

    return stacks


print('Part 1')
stacks, moves = read_input('05.txt', 9)
for m in moves:
    stacks = move_crates(m, stacks, 'one')
print(''.join([x[0] for x in stacks]))

print('Part 2')
stacks, moves = read_input('05.txt', 9)
for m in moves:
    stacks = move_crates(m, stacks, 'all')
print(''.join([x[0] for x in stacks]))