import numpy as np
from itertools import cycle
import matplotlib.pyplot as plt

#10007 cards, [0:]
# 0 starts at top
# first: new stack by reversing, top to bottom, etc.
# second: cut N cards, take top N cards and move them to bottom
#   can cut <0. last N go to top of new stack
# third: deal N: deal from top, every N, cycle around
#   one card per spot
#   collect left (top) to right (bottom)


def read_instructions(fn):
    instructions = []
    with open(fn) as fh:
        for l in fh:
            if l.startswith('cut'):
                inst = 'cut'
            elif l.startswith('deal with'):
                inst = 'dwi'
            elif l.startswith('deal into'):
                inst = 'dns'
            n = l.rstrip().split(' ')[-1]
            instructions.append((inst, n))
    return instructions


def deal_new_stack(deck, N=None):
    new_deck = np.flip(deck)
    return new_deck


def deal_new_stack_ind(deck_size, ind, N=None):
    new_ind = deck_size - ind - 1
    return new_ind


def cut_deck(deck, N):
    new_deck = np.roll(deck, -1 * N)
    return new_deck


def cut_deck_ind(deck_size, ind, N):
    N = N % deck_size
    new_ind = ind + N
    if new_ind > deck_size:
        new_ind = new_ind % deck_size
    return new_ind


def deal_with_increment(deck, N):
    deal_inds = cycle(range(len(deck)))
    deck = list(deck)
    new_deck = [0] * len(deck)
    while deck:
        ind = next(deal_inds)
        new_deck[ind] = deck.pop(0)
        for _ in range(N - 1):
            next(deal_inds)
    return np.array(new_deck)


def deal_with_increment_ind(deck_size, ind, N):
    for a in np.arange(np.ceil(-1 * ind / N),
                       np.floor(N - ind / deck_size) + 1):
        new_ind = (ind + a * deck_size) / N
        if new_ind > 0 and new_ind % 1 == 0:
            return int(new_ind)

def save_list(to_save, fn):
    with open(fn, 'w') as fh:
        for item in to_save:
            fh.write(str(item) + '\n')



# print('Part A')
# instructions_dict = {'cut': cut_deck,
#                      'dwi': deal_with_increment,
#                      'dns': deal_new_stack}
# deck_size = 10007
# deck = []
# for n in range(deck_size):
#     deck.append(n)
# deck = np.array(deck)

# instructions = read_instructions('22.txt')
# for inst, n in instructions:
#     # print(inst, n)
#     if inst == 'dns':
#         n = 0
#     deck = instructions_dict[inst](deck, int(n))

# print(np.where(deck == 2019))

print('Part B')
deck_size = 119315717514047
deck_size = 10007

instructions_dictb = {'cut': cut_deck_ind,
                      'dwi': deal_with_increment_ind,
                      'dns': deal_new_stack_ind}

# instructions = read_instructions('22_testorder.txt')
instructions = read_instructions('22.txt')
# instructions.reverse()
ind = 2020
pos_list = [ind]
pos_set = set([ind])
max_iter = 101741582076661
end_cond = False
# while not end_cond:
for _ in range(1):
    for inst, n in instructions:
        if inst == 'dns':
            n = 0
        ind = instructions_dictb[inst](deck_size, ind, int(n))
    # if ind in pos_set:
    #     end_cond = True
        pos_list.append(ind)
    # pos_set.add(ind)
print(ind)
# inst_count = {'cut': 0, 'dwi': 0, 'dns': 0}
# for inst, n in instructions:
#     if inst == 'dns':
#         inst_count[inst] += 1
#     else:
#         inst_count[inst] += int(n)

# print(inst_count)
# save_list(pos_list, '22_out1.txt') # run it backwards
# save_list(pos_list, '22_out2.txt') 
# save_list(pos_list, '22_out3.txt') # save each instruction
# # print(len(pos_list), len(set(pos_list)))
# plt.plot(pos_list, lw=0.2)
# plt.show()



# Notes
# Does not matter the order of adjacent cuts

# # Check against running forward
# instructions_dict = {'cut': cut_deck,
#                      'dwi': deal_with_increment,
#                      'dns': deal_new_stack}
# deck = []
# for n in range(deck_size):
#     deck.append(n)
# deck = np.array(deck)

# instructions = read_instructions('22.txt')
# for inst, n in instructions:
#     # print(inst, n)
#     if inst == 'dns':
#         n = 0
#     deck = instructions_dict[inst](deck, int(n))

# print(np.where(deck == 2241))




