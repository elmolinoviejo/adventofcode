def read_input(fn):
    inputs = []
    with open(fn) as fh:
        for line in fh.readlines():
            inputs.append(int(line.rstrip()))
    return inputs


def part1(inputs):
    for n1 in inputs:
        if 2020 - n1 in inputs:
            return(n1 * (2020 - n1))


def part2(inputs):
    for n1 in inputs:
        for n2 in inputs:
            if n2 > 2020 - n1:
                continue
            elif 2020 - n1 - n2 in inputs:
                return(n1 * n2 * (2020 - n1 - n2))


inputs = read_input('01.txt')
# Part 1
print(f'Part 1:\t{part1(inputs)}')
# Part 2
print(f'Part 2:\t{part2(inputs)}')
