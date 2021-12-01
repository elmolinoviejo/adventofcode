import re
from itertools import product
# from scipy.ndimage import center_of_mass
import numpy as np
from collections import deque


def load_bots(fn):
    bots = {}
    lines = [x for x in open(fn).read().split('\n')]
    for line in lines:
        pos = re.search(r'\<([\-\d\,]*)\>', line)[1]
        pos = tuple([int(x) for x in pos.split(',')])
        radius = int(line.split('=')[-1])
        bots[pos] = radius
    return bots


def dist(b1, b2):
    return sum([abs(x1 - x2) for x1, x2 in zip(b1, b2)])


def inrange(b1, bots):
    n = 0
    for b2 in bots:
        d = dist(b1, b2)
        if d <= bots[b1]:
            n += 1
    return n


def inrangeof(pos, bots):
    n = 0
    for b in bots:
        d = dist(pos, b)
        if d <= bots[b]:
            n += 1
    return n


# def next_pos(start, step, pos_ranges, bots):
#     # n = inrangeof(start, bots)
#     to_return = {}  # n: [positions]
#     # if start not in pos_ranges:
#     #     pos_ranges[start] = n
#     for diff in product((0, 1, -1), repeat=3):
#         if diff == (0, 0, 0):
#             continue
#         new_pos = tuple([x + y * step for x, y in zip(start, diff)])
#         if new_pos not in pos_ranges:
#             new_n = inrangeof(new_pos, bots)
#             pos_ranges[new_pos] = new_n
#         else:
#             new_n = pos_ranges[new_pos]

#         if new_n not in to_return:
#             to_return[new_n] = []
#         to_return[new_n].append(new_pos)
#     max_n = max(to_return.keys())
#     # if max_n <= n:
#     #     return max_n, False, pos_ranges

#     return max_n, to_return[max_n], pos_ranges

# version without dictionary of values
# 


bots = load_bots('23test2.txt')
bots = load_bots('23.txt')

# Part 1
max_r = max(bots.values())
max_b = [b for b, r in bots.items() if r == max_r][0]
print(f"Part 1:\t{inrange(max_b, bots)}")

# Part 2
diffs = []
for diff in product((0, 1, -1), repeat=3):
    if diff == (0, 0, 0):
        continue
    diffs.append(diff)

bot_list = []
for (x, y, z), r in bots.items():
    bot_list.append([x, y, z, 1 / (r ** 3)])
bot_arr = np.array(bot_list)

# com = center_of_mass(bot_arr, index=[0, 1,])
com = np.average(bot_arr[:, :3], axis=0, weights=bot_arr[:, 3])
# print(com)

ans = 0
com_loc = []
for v in com:
    ans += round(abs(v))
    com_loc.append(int(round(v)))
com_loc = tuple(com_loc)
print(com_loc)
# print(ans)

com_loc = (0, 0, 0)
# com_loc = (23501523, 10497974, 10027822)
# com_loc = (22750210, 9746661, 9276509)
# com_loc = (24252836, 11249287, 10779135)
com_loc = (24252560, 11249755, 10779014)
current_ans = inrangeof(com_loc, bots)
closest_dist = dist((0, 0, 0), com_loc)
print(f"first ans:\t{current_ans}")
print(f"closest dist:\t{closest_dist}")
old_dist = closest_dist
locs_range = {current_ans: [com_loc]}
checked = set()
to_check = deque([com_loc])


# move towards origin stop if inrange of goes down
loc = com_loc
ans = inrangeof(loc, bots)
step = 1
to_check = [loc]
checked = set()
while len(to_check) > 0:
    loc = to_check.pop()
    for d_ind in range(3):
        new_loc = list(loc)
        new_loc[d_ind] = new_loc[d_ind] - step
        new_loc = tuple(new_loc)
    new_ans = inrangeof(new_loc, bots)
    print(new_loc, new_ans)
    if new_ans < ans:
        print(loc, ans)
        break
    else:
        loc = new_loc
        ans = new_ans







# print(locs_range)
# now search around com for locs that have more
# for _ in range(1000):

# max_step = 10

# step = max_step
# n_same = 0
# while len(to_check) > 0:
#     loc = to_check.popleft()
#     # if loc in checked:
#     #     continue
#     checked.add(loc)
#     for diff in diffs:
#         new_loc = tuple([x + y * step for x, y in zip(loc, diff)])
#         loc_ans = inrangeof(new_loc, bots)
#         if new_loc in checked:
#             continue
#         if loc_ans < current_ans:
#             continue

#         new_dist = dist((0, 0, 0), new_loc)
#         if new_dist < closest_dist:
#             closest_dist = new_dist
#         if loc_ans not in locs_range:
#             locs_range[loc_ans] = []
#         # locs_range[loc_ans].append(new_loc)
#         if loc_ans > current_ans:
#             print('BETTER', loc_ans, new_loc)
#             step = max_step
#             n_same = 0
#             current_ans = loc_ans
#             best_loc = new_loc
#             closest_dist = new_dist
#             to_check = deque(
#                 [x for x in locs_range[loc_ans] if x not in checked])
#         elif loc_ans == current_ans:
#             # if new_dist <= closest_dist:
#             to_check.append(new_loc)
#     # print(closest_dist, old_dist)
#     if closest_dist == old_dist:
#         n_same += 1

#     if n_same > 1:
#         step = int(step / 1.1)
#         old_dist = closest_dist
#         n_same = 0
#         if step == 0:
#             step = 1
#     # else:
#     #     step = step * 2
#     old_dist = closest_dist
#     print('\t'.join([str(current_ans),
#                      str(len(to_check)),
#                      str(closest_dist),
#                      str(step), 
#                      str(len(checked))]))

# print(current_ans)
# print(new_loc)



# 5658529 too low
# 8944674 too low
# 7944674 
# 42611322 too low
# 46281258 wrong
# 46279329 wrong
# 45748547 wrong

# edge_lists = {0: [], 1: [], 2: []}
# for pos, r in bots.items():
#     for ind, p in enumerate(pos):
#         edge_lists[ind].extend([p + r, p - r])

# spans = []
# for ind in range(3):
#     spans.append(abs(min(edge_lists[ind]) - max(edge_lists[ind])))
# start_step = max(spans)
# print(start_step)







# start_step = 1
# step = start_step
# start = (0, 0, 0)
# pos_ranges = {}
# max_n = inrangeof(start, bots)
# queue = [start]
# n_iter = 1

# # count up or count

# while True:
#     print(max_n, queue, n_iter)
#     if n_iter >= start_step:
#         break
#     # print(max_n, queue)
#     start = queue.pop()
#     n, next_ps, pos_ranges = next_pos(start, step, pos_ranges, bots)
#     if n > max_n:
#         max_n = n
#         queue.extend(next_ps)
#         step = start_step
#         n_iter = 1
#     else:
#         queue.append(start)
#         step -= 1
#         n_iter += 1
# print(max_n, queue)


# def gradient_descent(start, max_step, bots):
#     step = max_step
#     max_n = inrangeof(start, bots)
#     queue = [start]

#     while True:
#         if step == 1:  #is this right?
#             return queue

#     return None


# try with sets - NO
# try with weight center of mass


# def centerofmass(bots):
#     total_mass = 0
#     weighted_locs = [0, 0, 0]
#     for loc, r in bots.items():
#         total_mass += 1 / r
#         for ind in range(3):
#             weighted_locs[ind] = weighted_locs[ind] + loc[ind]
#     com = tuple([(1 / total_mass) * d for d in weighted_locs])
#     return com
