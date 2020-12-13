def read_commands(fn):
    lines = [g for g in open(fn).read().split('\n')]
    return [(line[0], int(line[1:])) for line in lines]


def rotate1(loc, direction, command):
    c, val = command
    if c == 'L':
        exp = val / 90
    elif c == 'R':
        exp = (360 - val) / 90
    new_direction = direction * (1j ** exp)
    return loc, new_direction


def move1(loc, direction, command):
    c, val = command
    direction_lookup = {'N': 1j,
                        'S': -1j,
                        'E': 1,
                        'W': -1}
    new_loc = loc + direction_lookup[c] * val
    return new_loc, direction


def step1(loc, direction, command):
    c, val = command
    new_loc = loc + direction * val
    return new_loc, direction


def run_commands1(fn, start_params):
    commands = read_commands(fn)
    loc, direction = start_params
    for command in commands:
        c, val = command
        if c in 'NSEW':
            move_func = move1
        elif c in 'LR':
            move_func = rotate1
        else:
            move_func = step1
        loc, direction = move_func(loc, direction, command)
    return loc


def rotate2(loc, rel_wp, command):
    c, val = command
    if c == 'L':
        exp = val / 90
    elif c == 'R':
        exp = (360 - val) / 90
    new_rel_wp = rel_wp * (1j ** exp)
    return loc, new_rel_wp


def move2(loc, rel_wp, command):
    c, val = command
    direction_lookup = {'N': 1j,
                        'S': -1j,
                        'E': 1,
                        'W': -1}
    new_rel_wp = rel_wp + direction_lookup[c] * val
    return loc, new_rel_wp


def step2(loc, rel_wp, command):
    c, val = command
    new_loc = loc + rel_wp * val
    return new_loc, rel_wp


def run_commands2(fn, start_params):
    commands = read_commands(fn)
    loc, rel_wp = start_params
    for command in commands:
        c, val = command
        if c in 'NSEW':
            move_func = move2
        elif c in 'LR':
            move_func = rotate2
        else:
            move_func = step2
        loc, rel_wp = move_func(loc, rel_wp, command)
    return loc


start_params = (0, 1)
final_loc = run_commands1('12.txt', start_params)
print(f"Part 1:\t{int(abs(final_loc.real) + abs(final_loc.imag))}")

start_params = (0, 10 + 1j)
final_loc = run_commands2('12.txt', start_params)
print(final_loc)
print(f"Part 2:\t{int(abs(final_loc.real) + abs(final_loc.imag))}")
