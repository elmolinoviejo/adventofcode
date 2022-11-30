def read_input(fn):
    inputs = []
    with open(fn) as fh:
        for line in fh.readlines():
            inputs.append(int(line.rstrip()))
    return inputs

