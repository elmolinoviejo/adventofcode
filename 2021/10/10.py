def get_lines(fn):
    with open(fn) as fh:
        lines = fh.read().split('\n')
    return lines


def check_line(line):
    close_open = dict(zip(')]}>', '([{<'))
    order = []
    for s in line:
        if s in '([{<':
            order.append(s)
        else:
            if order.pop() != close_open[s]:
                return True, s
    return False, order


def corrupt_score(s):
    score_vals = dict(zip(')]}>', [3, 57, 1197, 25137]))
    return score_vals[s]


def incomplete_score(order):
    score_vals = dict(zip('([{<', [1, 2, 3, 4]))
    order.reverse()
    score = 0
    for s in order:
        score = score * 5 + score_vals[s]
    return score


fn = '10.txt'
lines = get_lines(fn)
ans1 = 0
inscores = []
for line in lines:
    corrupt, s = check_line(line)
    if corrupt:
        ans1 += corrupt_score(s)
    else:
        inscores.append(incomplete_score(s))

print(ans1)
inscores.sort()
print(inscores[int((len(inscores) - 1) / 2)])
