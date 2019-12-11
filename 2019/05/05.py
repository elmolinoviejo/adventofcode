import sys
sys.path.append('../')
import intcode2019 as ic

fn = '05_test1.txt'
fn = '05.txt'

print('Part A')
p = ic.input_to_program(fn)
input_val = 1
c = ic.Computer(p, input_val)

while c.opcode != 99:
    c.run_op(verbose=False)
print(c.output_val)

print('Part B')
p = ic.input_to_program(fn)
input_val = 5
c = ic.Computer(p, input_val)

while c.opcode != 99:
    c.run_op(verbose=False)
print(c.output_val)
