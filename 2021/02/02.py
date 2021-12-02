def read_input(fn):
    inputs = []
    with open(fn) as fh:
        for line in fh.readlines():
            inputs.append(tuple(line.rstrip().split(' ')))
    return inputs


def dive_step(loc, command, aim=False):
    direction = command[0]
    distance = int(command[1])
    if aim is False:
        if direction == 'up':
            loc = (loc[0], loc[1] - distance)
        elif direction == 'down':
            loc = (loc[0], loc[1] + distance)
        elif direction == 'forward':
            loc = (loc[0] + distance, loc[1])

    else:
        if direction == 'up':
            aim -= distance
        elif direction == 'down':
            aim += distance
        elif direction == 'forward':
            loc = (loc[0] + distance,
                   loc[1] + (aim * distance))

    return loc, aim


commands = read_input('02.txt')

# Part One
loc = (0, 0)
for command in commands:
    loc, _ = dive_step(loc, command)
print(loc[0] * loc[1])

# Part Two
loc = (0, 0)
aim = 0
for command in commands:
    loc, aim = dive_step(loc, command, aim)
print(loc[0] * loc[1])
