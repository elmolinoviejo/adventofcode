import sys
from itertools import cycle
sys.path.append('../')
import intcode2019 as ic


# TODO rewrite to use Network_Node class
class Network_Node:
    def __init__(self, fn, nad):
        self.nad = nad
        program = ic.input_to_program(fn)
        self.computer = ic.Computer(program, input_val=nad)
        self.input_queue = []
        self.first_input = True
        self.output_counter_cycle = cycle([0, 1, 2])
        self.output_counter = next(self.output_counter_cycle)
        self.current_output = None
        self.last_action_receive = True
        self.last_receive_count = 0
        
def get_next_input(input_queues, nad):
    if len(input_queues[nad]) > 0:
        input_val = input_queues[nad][0]
        queue_check = True
    else:
        input_val = -1
        queue_check = False
    return input_val, queue_check


print('Part A')
fn = '23.txt'
program = ic.input_to_program(fn)

computers = dict()
input_queues = dict()
input_from_queue = dict()
first_input = dict()
output_counter_cycles = dict()
output_counter = dict()
current_output = dict()
last_action_receive = dict()
last_receive_count = dict()

nat_vals = [-1, -1]


for nad in range(50):
    program = ic.input_to_program(fn)
    computers[nad] = ic.Computer(program, input_val=nad)
    input_queues[nad] = []
    input_from_queue[nad] = False
    first_input[nad] = True
    output_counter_cycles[nad] = cycle([0, 1, 2])
    output_counter[nad] = next(output_counter_cycles[nad])
    current_output[nad] = None
    last_action_receive[nad] = True
    last_receive_count[nad] = 0

y_vals = set()
end_cond = False
while not end_cond:
    # check for NAT conditions
    if (min(last_receive_count.values()) > 10 and
        max([len(q) for q in input_queues.values()]) == 0):
        input_queues[0].extend(nat_vals)
        if nat_vals[1] != -1:
            y_vals.add(nat_vals[1])
            print(nat_vals[1])
            print(len(y_vals))
        nat_vals = [-1, -1]        

        # print(len(y_vals))

# for _ in range(10000):
    for nad, c in computers.items():
        

            # end_cond = True
        # check for input queue
        queue_check = False
        if not first_input[nad]:
            input_val, queue_check = get_next_input(input_queues, nad)
            # print(input_val)
            c.input_val = input_val

        c.run_op()
        if c.opcode == 3:
            first_input[nad] = False
            if queue_check:
                input_queues[nad].pop(0)
            last_action_receive[nad] = True
            last_receive_count[nad] += 1
        if c.opcode == 4:
            if output_counter[nad] == 0:
                current_output[nad] = [c.output_val]
            elif output_counter[nad] == 1:
                current_output[nad].append(c.output_val)
            elif output_counter[nad] == 2:
                current_output[nad].append(c.output_val)
                if current_output[nad][0] == 255:
                    nat_vals = current_output[nad][1:]
                    # print(nat_vals)
                else:
                    input_queues[current_output[nad][0]].extend(
                        current_output[nad][1:])
            output_counter[nad] = next(output_counter_cycles[nad])
            last_action_receive[nad] = False
            last_receive_count[nad] = 0
    # print(sum(last_action_receive.values()))
# [print(c.program[62]) for c in computers.values()]
# print(computers)
