def load_input(fn):
    dots = set()
    folds = []
    with open(fn) as fh:
        in1, in2 = fh.read().split('\n\n')
        for l in in1.split('\n'):
            dots.add(tuple([int(x) for x in l.split(',')]))
        for l in in2.split('\n'):
            f = l.split('fold along ')[1]
            f = f.split('=')
            folds.append(tuple([f[0], int(f[1])]))
    return dots, folds


def fold(dots, f):
    new_dots = set()
    fdir, fn = f
    for d in dots:
        x, y = d
        if fdir == 'x':
            if x < fn:
                new_dots.add(d)
            else:
                new_dots.add((fn - (x - fn), y))
        if fdir == 'y':
            if y < fn:
                new_dots.add(d)
            else:
                new_dots.add((x, fn - (y - fn)))
    return new_dots


def print_dots(dots):
    maxx = max([x for x, y in dots])
    maxy = max([y for x, y in dots])

    out = ''
    for y in range(maxy + 1):
        for x in range(maxx + 1):
            if (x, y) in dots:
                out += '}{'
            else:
                out += '  '
        out += '\n'
    print(out)


fn = '13.txt'
dots, folds = load_input(fn)
for ind, f in enumerate(folds):
    dots = fold(dots, f)
    if ind == 0:
        print(len(dots))
print_dots(dots)
