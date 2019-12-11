import sys
sys.path.append('../')
import intcode2019 as ic

fn = '02.txt'

# Part A
print('Part A')
p = ic.input_to_program(fn)
c = ic.Computer(p)
noun, verb = 12, 2
c.program[1] = noun
c.program[2] = verb
while c.opcode != 99:
    c.run_op(verbose=False)
print(c.program[0])

# Part B
print('Part B')
for noun in range(100):
    for verb in range(100):
        p = ic.input_to_program(fn)
        c = ic.Computer(p)
        c.program[1] = noun
        c.program[2] = verb
        while c.opcode != 99:
            c.run_op(verbose=False)
        if c.program[0] == 19690720:
            answer = 100 * noun + verb

print(answer)
