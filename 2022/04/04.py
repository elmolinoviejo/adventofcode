def read_input(fn):
    sections = []
    with open(fn) as fh:
        games = fh.read().split('\n')
        for g in games:
            moves.append(tuple(g.split(' ')))

    return moves