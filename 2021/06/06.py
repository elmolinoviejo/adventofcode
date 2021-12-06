from collections import Counter


def get_input(fn):
    with open(fn) as fh:
        fish = [int(x) for x in fh.read().rstrip().split(',')]
        return fish


def next_day(fc):
    nfc = Counter({k: 0 for k in range(9)})
    for k, v in fc.items():
        if k == 0:
            nfc[8] += v
            nfc[6] += v
        else:
            nfc[k - 1] += v
    return nfc


def count_fish(fc):
    return sum([v for v in fc.values()])


fn = '06.txt'

fish = get_input(fn)
fc = Counter(fish)
for _ in range(80):
    fc = next_day(fc)
print(count_fish(fc))

fish = get_input(fn)
fc = Counter(fish)
for _ in range(256):
    fc = next_day(fc)
print(count_fish(fc))
