def read_input(fn):
    in_out = []
    with open(fn) as fh:
        for line in fh.readlines():
            in_out.append(x.split() for x in line.split(' | '))
    return in_out


