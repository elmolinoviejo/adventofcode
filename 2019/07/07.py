import sys
sys.path.append('../')
import intcode2019 as ic
from itertools import permutations, cycle
# from collections import deque
import numpy as np


fn = '07.txt'
program = ic.input_to_program(fn)

amp_cycle = cycle(range(5))
previous_amp = dict(zip((0, 1, 2, 3, 4), (4, 0, 1, 2, 3)))

# Part A
permute_phases = permutations(range(5))
output_vals = []
for phases in permute_phases:
    amps = dict(zip(range(5), [ic.Computer(program.copy())
                               for _ in range(5)]))
    amp_no = next(amp_cycle)
    # Initialize computer inputs with the phase settings
    for c, p in zip(amps.keys(), phases):
        amps[c].input_val = p
        amps[c].use_phase = True
    # Run each amp once
    for amp_no, current_c in amps.items():
        while current_c.opcode != 99:
            current_c.run_op(verbose=False)
            # Switch from phase to input
            # on the first instance of opcode 3
            if current_c.opcode == 3 and current_c.use_phase:
                current_c.use_phase = False
                if amp_no == 0:
                    current_c.input_val = 0
                else:
                    current_c.input_val = amps[
                        previous_amp[amp_no]].output_val
    output_vals.append(amps[4].output_val)

print('Part A')
print(max(output_vals))

# Part B

fn = '07.txt'
program = ic.input_to_program(fn)


previous_amp = dict(zip((0, 1, 2, 3, 4), (4, 0, 1, 2, 3)))

permute_phases = permutations(np.arange(5, 10))
output_vals = []
for phases in permute_phases:
# for phases in [(9, 8, 7, 6, 5)]:
    amps = dict(zip(range(5), [ic.Computer(program.copy())
                               for _ in range(5)]))
    amp_cycle = cycle(range(5))
    amp_no = next(amp_cycle)  # cycle by -1
    # Initialize computer inputs with the phase settings
    for c, p in zip(amps.keys(), phases):
        amps[c].input_val = p
        amps[c].use_phase = True
    # Run amps until one throws opcode 99
    while all([c.opcode != 99 for c in amps.values()]):
        current_c = amps[amp_no]
        current_c.run_op(verbose=False)
        # Switch from phase to input
        # on the first instance of opcode 3 per amp
        if current_c.opcode == 3 and current_c.use_phase:
            current_c.use_phase = False
            if amp_no == 0:
                current_c.input_val = 0
            else:
                current_c.input_val = amps[
                    previous_amp[amp_no]].output_val
        if current_c.opcode == 4:
            amp_no = next(amp_cycle)
            if not amps[amp_no].use_phase:
                amps[amp_no].input_val = amps[
                    previous_amp[amp_no]].output_val
    # print(phases, amps[4].output_val)
    output_vals.append(amps[4].output_val)

print('Part B')
print(max(output_vals))
