def read_input(fn):
    sums = []
    with open(fn) as fh:
        elves = fh.read().split('\n\n')
        for e in elves:
            sums.append(sum([int(x) for x in e.split('\n')]))
    return sums

sums = read_input('01.txt')

print('Part 1:')
print(max(sums))

print('Part 2:')
sums.sort()
print(sum(sums[-3:]))
