import sys
sys.path.append('../')
import intcode2019 as ic


def find_scaffold_intersections(output_array):
    intersections = []
    scaffold_chars = '#><^v'
    for (x, y), char in output_array.items():
        if char in scaffold_chars:
            is_intersection = True
            for adj_loc in [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]:
                if adj_loc not in output_array:
                    is_intersection = False
                elif output_array[adj_loc] not in scaffold_chars:
                    is_intersection = False
            if is_intersection:
                intersections.append((x, y))
    return intersections

# Part A
print('Part A')
fn = '17.txt'
program = ic.input_to_program(fn)
input_val = 1
c = ic.Computer(program, input_val)

output_string = ''
output_array = dict()
x, y = 0, 0
while c.opcode != 99:
    c.run_op(verbose=False)
    if c.opcode == 4:
        output_char = chr(c.output_val)
        output_string += output_char
        if output_char != '\n':
            output_array[(x, y)] = output_char
            x += 1
        else:
            x = 0
            y += 1

scaff_ints = find_scaffold_intersections(output_array)
ans = 0
for (x, y) in scaff_ints:
    ans += x*y

print(ans)

with open('17_map.txt', 'w') as fh:
    fh.write(output_string)

# Part B
# Get the patterns manually
print('Part B')
fn = '17.txt'
program = ic.input_to_program(fn)
input_val = 1
c = ic.Computer(program, input_val)
c.program[0] = 2

main_routine = 'A,B,A,C,C,A,B,C,B,B'
func_A = 'L,8,R,10,L,8,R,8'
func_B = 'L,6,6,R,8,R,8'
func_C = 'L,8,R,6,R,6,R,10,L,8'

main_routine = [ord(x) for x in main_routine]
main_routine.append(ord('\n'))

funcA = [ord(x) for x in func_A]
funcA.append(ord('\n'))

funcB = [ord(x) for x in func_B]
funcB.append(ord('\n'))

funcC = [ord(x) for x in func_C]
funcC.append(ord('\n'))

video = [ord('n'), ord('\n')]

input_order = [main_routine, funcA, funcB, funcC, video]
input_order_ind = 0
input_ind = 0
input_switch = False

output_stringB = ''

while c.opcode != 99:
    c.run_op(verbose=False)
    if c.opcode == 3:
        if input_ind > (len(input_order[input_order_ind]) - 1):
            input_switch = False
            input_order_ind += 1
            input_ind = 0
        if input_switch:
            c.input_val = input_order[input_order_ind][input_ind]
            input_ind += 1

    if c.opcode == 4:
        if chr(c.output_val) == ':':
            input_switch = True
            c.input_val = input_order[input_order_ind][input_ind]
            input_ind += 1
        output_stringB += chr(c.output_val)

print(c.output_val)
