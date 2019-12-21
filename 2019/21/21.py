import sys
sys.path.append('../')
import intcode2019 as ic


def input_to_ascii(input_strs):
    input_ascii = []
    for input_str in input_strs:
        for s in input_str:
            input_ascii.append(ord(s))
        input_ascii.append(10)
    return input_ascii


def output_to_str(output_ascii, print_switch=True):
    output_str = ''
    for a in output_ascii:
        output_str += chr(a)
    return output_str
    if print_switch:
        print(output_str)


print('Part A')
fn = '21.txt'
program = ic.input_to_program(fn)
c = ic.Computer(program)
output_ascii = []

input_strs = ['NOT A J',
              'NOT B T',
              'NOT C T',
              'OR T J',
              'AND D J',
              'WALK']
input_ascii = input_to_ascii(input_strs)
input_ind = 0

while c.opcode != 99:
    c.run_op()
    if c.opcode == 4:
        output_ascii.append(c.output_val)
        if c.output_val == 58:
            c.input_val = input_ascii[input_ind]
    if c.opcode == 3:
        if input_ind == len(input_ascii) - 1:
            continue
        else:
            input_ind += 1
            c.input_val = input_ascii[input_ind]

try:
    output_str = output_to_str(output_ascii)
    print(output_str)
except ValueError:
    print(output_ascii[-1])

print('Part B')
fn = '21.txt'
program = ic.input_to_program(fn)
c = ic.Computer(program)
output_ascii = []

input_strs = ['NOT A J',
              'NOT B T',
              'OR T J',
              'NOT C T',
              'OR T J',
              'NOT E T',
              'NOT T T',
              'OR H T',
              'AND T J',
              'AND D J',
              'RUN']
input_ascii = input_to_ascii(input_strs)
input_ind = 0

while c.opcode != 99:
    c.run_op()
    if c.opcode == 4:
        output_ascii.append(c.output_val)
        if c.output_val == 58:
            c.input_val = input_ascii[input_ind]
    if c.opcode == 3:
        if input_ind == len(input_ascii) - 1:
            continue
        else:
            input_ind += 1
            c.input_val = input_ascii[input_ind]

try:
    output_str = output_to_str(output_ascii)
    print(output_str)
except ValueError:
    print(output_ascii[-1])
