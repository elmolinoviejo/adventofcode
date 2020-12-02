def input_to_pw_tuples(fn):
    pw_tuples = []
    with open(fn) as fh:
        for line in fh.readlines():
            line_split = line.rstrip().split(' ')

            min_max = [int(x) for x in line_split[0].split('-')]
            letter = line_split[1][0]
            pw = line_split[2]

            pw_tuples.append(tuple([min_max, letter, pw]))

    return pw_tuples


def part1(pw_tuples):
    n_valid = 0
    for min_max, letter, pw in pw_tuples:
        letter_count = pw.count(letter)
        if (letter_count >= min_max[0]):
            if letter_count <= min_max[1]:
                n_valid += 1
    return n_valid


def part2(pw_tuples):
    n_valid = 0
    for min_max, letter, pw in pw_tuples:
        pos_letters = pw[min_max[0] - 1] + pw[min_max[1] - 1]
        if pos_letters.count(letter) == 1:
            n_valid += 1
    return n_valid


pw_tuples = input_to_pw_tuples('02.txt')
# Part 1
print('Part 1:')
print(part1(pw_tuples))
print('Part 2:')
print(part2(pw_tuples))
