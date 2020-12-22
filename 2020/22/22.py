from collections import deque
from copy import deepcopy


def load_cards(fn):
    decks = {0: [], 1: []}
    for dnum, clist in enumerate(open(fn).read().split('\n\n')):
        for c in clist.split('\n'):
            if c[0] == 'P':
                continue
            decks[dnum].append(int(c))
    return deque(decks[0]), deque(decks[1])


def game1(c1, c2):
    while (len(c1) > 0) and (len(c2) > 0):
        n1, n2 = c1.popleft(), c2.popleft()
        if n1 > n2:
            [c1.append(n) for n in (n1, n2)]
        else:
            [c2.append(n) for n in (n2, n1)]
    if c1 > c2:
        winner = 1
    else:
        winner = 2
    return winner, c1, c2


def winner_score(c1, c2):
    if len(c1) > len(c2):
        cards = c1
    else:
        cards = c2

    ans = 0
    for ind, val in enumerate(cards):
        ans += (len(cards) - ind) * val
    return ans


def c2hash(c1, c2):
    h = ','.join([','.join([str(c) for c in c1]),
                  'x',
                  ','.join([str(c) for c in c2])])
    return h


# FIX THIS
def game2(c1, c2):
    card_orders = []
    c1, c2 = deepcopy(c1), deepcopy(c2)
    while (len(c1) > 0) and (len(c2) > 0):
        h = c2hash(c1, c2)
        if h in card_orders:
            return 1, c1, c2
        card_orders.append(h)
        n1, n2 = c1.popleft(), c2.popleft()
        if (n1 > len(c1)) or (n2 > len(c2)):
            if n1 > n2:
                winner = 1
            else:
                winner = 2
        else:
            subc1 = deque(list(c1)[:n1])
            subc2 = deque(list(c2)[:n2])
            winner, _, _ = game2(subc1, subc2)
        if winner == 1:
            [c1.append(n) for n in (n1, n2)]
        else:
            [c2.append(n) for n in (n2, n1)]
    if len(c1) > len(c2):
        return 1, c1, c2
    else:
        return 2, c1, c2


# Part 1
c1, c2 = load_cards('22.txt')
winner, c1, c2 = game1(c1, c2)
ans1 = winner_score(c1, c2)
print(f"Part 1:\t{ans1}")

# Part 2
c1, c2 = load_cards('22.txt')
winner, c1, c2 = game2(c1, c2)
ans2 = winner_score(c1, c2)
print(f"Part 2:\t{ans2}")
