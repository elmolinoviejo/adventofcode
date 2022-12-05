import string


def read_input(fn):
    moves = []
    with open(fn) as fh:
        rucksacks = fh.read().split('\n')
    return rucksacks

def score(lett):
    scores = {}
    scores.update(dict(zip(string.ascii_lowercase, range(1, 27))))
    scores.update(dict(zip(string.ascii_uppercase, range(27, 53))))
    return scores[lett]

rss = read_input('03.txt')

print('Part 1')
ans = 0
for rs in rss:
    l = len(rs)
    lett = set(rs[:int(l/2)]) & set(rs[int(l/2):])
    ans += score(lett.pop())
print(ans)

print('Part 2')
ans = 0
for ind in range(0, len(rss), 3):
    r1, r2, r3 = rss[ind], rss[ind + 1], rss[ind + 2]
    lett = set(r1) & set(r2) & set(r3)
    ans += score(lett.pop())
print(ans)
