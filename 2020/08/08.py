from copy import deepcopy


def input_to_program(fn):
    program = [g.split(' ') for g in open(fn).read().split('\n')]
    program = [tuple([x[0], int(x[1])]) for x in program]
    return program


def run_program(program):
    a = 0  # accumulator
    ind = 0
    ind_order = []
    first_run = True
    while first_run:
        if ind in ind_order:
            # program will repeat
            first_run = False
            return a, False
        elif ind == len(program):
            # program will end on final line
            return a, True
        else:
            ind_order.append(ind)

        step, val = program[ind]
        if step == 'acc':
            a += val
            ind += 1
        elif step == 'nop':
            ind += 1
        elif step == 'jmp':
            ind += val


def modulate_program(program):
    for ind, p in enumerate(program):
        temp_program = deepcopy(program)
        if p[0] == 'nop':
            temp_program[ind] = ('jmp', p[1])
        elif p[0] == 'jmp':
            temp_program[ind] = ('nop', p[1])
        else:
            continue

        a, end = run_program(temp_program)
        if end:
            return a


program = input_to_program('08.txt')
print(f"Part A:\t{run_program(program)[0]}")
print(f"Part B:\t{modulate_program(program)}")
