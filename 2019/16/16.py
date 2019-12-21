import numpy as np
from itertools import cycle


def read_signal(fn):
    with open(fn) as fh:
        signal = fh.readline().rstrip()
    return signal


def calc_position(input_signal, pos):
    n_repeat = pos + 1
    pattern = cycle([0, 1, 0, -1])
    adj_pattern = []
    while len(adj_pattern) < len(input_signal) + 1:
        adj_pattern.extend([next(pattern)] * n_repeat)
    adj_pattern = adj_pattern[1:]
    pos_output = 0
    for x, p in zip(input_signal, adj_pattern):
        pos_output += x * p
    pos_output = int(str(pos_output)[-1])
    return pos_output


def fft(input_signal):
    output_signal = []
    for pos, x in enumerate(input_signal):
        output_signal.append(calc_position(input_signal, pos))
    return output_signal


def fft_partb(input_signal):
    output_signal = np.empty_like(input_signal)
    for pos, x in enumerate(input_signal):
        if pos == 0:
            output_val = int(x)
        else:
            output_val = int(output_signal[pos - 1] + x)
        output_signal[pos] = int(str(output_val)[-1])
    return output_signal


print('Part A')
signal = read_signal('16.txt')
signal = [int(x) for x in signal]

for _ in range(100):
    signal = fft(signal)
print(''.join([str(x) for x in signal[:8]]))

print('Part B')
signal = read_signal('16.txt')
answer_offset = int(signal[:7])
signal = [int(x) for x in signal]

signal.reverse()
signal_cycle = cycle(signal)
sig_array = np.zeros((len(signal) * 10000) - answer_offset, dtype=np.int32)

for ind, _ in enumerate(sig_array):
    sig_array[ind] = next(signal_cycle)

for _ in range(100):
    sig_array = fft_partb(sig_array)

print(''.join([str(x) for x in sig_array[-1:-9:-1]]))
