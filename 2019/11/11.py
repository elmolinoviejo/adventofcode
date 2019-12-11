import sys
import numpy as np
import matplotlib.pyplot as plt
from itertools import cycle
sys.path.append('../')
import intcode2019 as ic


class Field:
    def __init__(self):
        self.direction = (0, 1)  # (x, y)
        self.location = (0, 0)
        self.colors = dict()
        self.colors[self.location] = 0

    def rotate_move(self, rotate_val):
        if rotate_val == 0:
            self.direction = (-1*self.direction[1], self.direction[0])
        elif rotate_val == 1:
            self.direction = (self.direction[1], -1*self.direction[0])
        self.location = (self.location[0] + self.direction[0],
                         self.location[1] + self.direction[1])
        if self.location not in self.colors:
            self.color(0)

    def color(self, color_val):
        self.colors[self.location] = color_val

    def return_image(self):
        # array size
        xvals = [loc[0] for loc in self.colors.keys()]
        yvals = [loc[1] for loc in self.colors.keys()]
        minx, maxx = min(xvals), max(xvals)
        miny, maxy = min(yvals), max(yvals)
        img = np.zeros((maxy-miny+1, maxx-minx+1))
        for loc, val in self.colors.items():
            img[loc[1]-miny, loc[0]-minx] = val
        plt.imshow(np.flip(img, 0))
        plt.show()

print('Part A')
fn = '11.txt'
program = ic.input_to_program(fn)
input_val = 1
c = ic.Computer(program, input_val)
f = Field()

locations = []
output_counters = cycle([0, 1])
output_counter = next(output_counters)
while c.opcode != 99:
    if output_counter == 0:
        c.input_val = f.colors[f.location]
    c.run_op(verbose=False)
    if c.opcode == 4:
        if output_counter == 0:
            color = c.output_val
            f.color(color)
        elif output_counter == 1:
            rotate_val = c.output_val
            f.rotate_move(rotate_val)
            if f.location not in locations:
                locations.append(f.location)
        output_counter = next(output_counters)
#         print(output_counter)

print(len(locations) - 1)

print('Part B')
fn = '11.txt'
program = ic.input_to_program(fn)
input_val = 1
c = ic.Computer(program, input_val)
f = Field()
f.colors[f.location] = 1

locations = []
output_counters = cycle([0, 1])
output_counter = next(output_counters)
while c.opcode != 99:
    if output_counter == 0:
        c.input_val = f.colors[f.location]
    c.run_op(verbose=False)
    if c.opcode == 4:
        if output_counter == 0:
            color = c.output_val
            f.color(color)
        elif output_counter == 1:
            rotate_val = c.output_val
            f.rotate_move(rotate_val)
            if f.location not in locations:
                locations.append(f.location)
        output_counter = next(output_counters)
#         print(output_counter)

f.return_image()
