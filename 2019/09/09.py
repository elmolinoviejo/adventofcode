import sys
sys.path.append('../')
import intcode2019 as ic

# Part A
print('Part A')
fn = '09.txt'
program = ic.input_to_program(fn)
input_val = 1
c = ic.Computer(program, input_val)

while c.opcode != 99:
    c.run_op(verbose=False)
print(c.output_val)

# Part B
print('Part B')
fn = '09.txt'
program = ic.input_to_program(fn)
input_val = 2
c = ic.Computer(program, input_val)

while c.opcode != 99:
    c.run_op(verbose=False)
print(c.output_val)
