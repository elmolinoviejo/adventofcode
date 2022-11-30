from collections import Counter
from itertools import cycle, islice, product

# Part One
start = (10, 7)
# start = (4, 8)

scores = {0: 0, 1: 0}
players = cycle(range(2))
nrolls = 0

boards = (cycle(range(1, 11)), cycle(range(1, 11)))
d = cycle(range(1, 101))

for _ in range(start[0]):
    next(boards[0])
for _ in range(start[1]):
    next(boards[1])

while max(scores.values()) < 1000:
    p = next(players)
    move = 0
    for _ in range(3):
        move += next(d)
        nrolls += 1
    for _ in range(move):
        score = next(boards[p])
    scores[p] += score
#     print(scores)
print('Part one:')
print(min(scores.values()) * nrolls)
print()


# Part Two

def get_roll_counts():
    rsums = []
    for rolls in product(range(1, 4),
                         range(1, 4),
                         range(1, 4)):
        rsums.append(sum(rolls))
    return Counter(rsums)


def move_board(start, n):
    board = cycle(range(1, 11))
    return next(islice(board, start + n - 1, start + n))


# def n_winners(score_spots, win=21):
#     ans = 0
#     winds = [v for k, v in score_spots.items() if k >= win]
#     for v in winds:
#         ans += sum(v.values())
#     return ans


# Logic on the winners is wrong, vastly overcounting
def step_add_winners(score_spots, n_prev_rolls):
    '''
    score_spots: dict of dicts
        score: {spot: count}
    '''
    n_wins = 0  # actual count of wins
    n_next_rolls = 0  # n of rolls that don't win this round
    init_score_spots = score_spots.copy()
    score_spots = {}
    for score0, spot_counts in init_score_spots.items():
        # for each previous score
        for start, startc in spot_counts.items():
            # for each board spot for that score
            for roll, rollc in rcount.items():
                # for all possible next rolls
                b = move_board(start, roll)
                score = score0 + b
                score_count = rollc * startc * n_prev_rolls
                # print(score0, start, startc)
                # print(score, b, rollc, score_count)
                # print()
                if score >= 21:
                    n_wins += int(score_count / n_prev_rolls)
                else:
                    n_next_rolls += rollc
                    # generate or fill dictionary with new score, board, counts
                    if score not in score_spots:
                        score_spots[score] = {}
                    if b not in score_spots[score]:
                        score_spots[score][b] = 0
                    score_spots[score][b] += score_count

    return score_spots, n_wins, n_next_rolls


# test
ss1 = {19: {4: 1}}  # score: {spot:count}
ss2 = {0: {8: 1}}  # score: {spot:count}

# ss1 = {0: {10: 1}} # score: {spot:count}
# ss2 = {0: {7: 1}} # score: {spot:count}

p_score_spots = {0: ss1, 1: ss2}
wins = {0: 0, 1: 0}
n_prev_rolls = 1
players = cycle(range(2))
rcount = get_roll_counts()
n_turns = 0
while len(p_score_spots[0]) > 0 and len(p_score_spots[1]) > 0:
# for _ in range(1):
    n_turns += 1
    p = next(players)
    ss = p_score_spots[p]
    ss, n_wins, n_prev_rolls = step_add_winners(ss, n_prev_rolls)
    # n_prev_rolls = 27 - nwrolls
    # n_prev_rolls = 1
    p_score_spots[p] = ss
    wins[p] += n_wins
    print()
    print(p, n_wins, n_prev_rolls)
    print(p_score_spots[p])
    # print(len(p_score_spots[0]), len(p_score_spots[1]))
    print(wins)

print('\n\nFINAL:')
print(f'turns: {n_turns}')
for p, scores in p_score_spots.items():
    print(p)
    print(scores)
    print()
print(wins)

# still too high, something wrong with previous rolls

