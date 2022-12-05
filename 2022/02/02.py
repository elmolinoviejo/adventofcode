from itertools import cycle, islice


def read_input(fn):
    moves = []
    with open(fn) as fh:
        games = fh.read().split('\n')
        for g in games:
            moves.append(tuple(g.split(' ')))

    return moves

def score_move(move):
    
    choice_score = dict(zip('XYZ', range(1,4)))

    a, b  = move

    # score for each choice
    score = choice_score[b]

    # score for game outcome
    opp_cyc = cycle('ABC')
    opp = islice(opp_cyc, choice_score[b] + 1, None)
    for step in [2, 1, 0]:
        opp_match = next(opp)
        # print(opp_match)
        if opp_match==a:
            score += step * 3
            return score

def get_choice(move):
    a, outcome  = move

    step = zip('XYZ', )

    opp_cyc = cycle('XYZ')
    opp = islice(opp_cyc, choice_score[a] + 1, None)

moves = read_input('02.txt')

print('Part 1')
ans = sum([score_move(m) for m in moves])
print(ans)
print('Part 2')
