import sys
from itertools import cycle
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from copy import deepcopy
sys.path.append('../')
import intcode2019 as ic


class Ball():

    def __init__(self, loc=None, direction=[0, 0]):
        self.loc = loc
        self.direction = direction

    def update_loc(self, new_loc):
            self.direction = [new_loc[0] - self.loc[0],
                              new_loc[1] - self.loc[1]]
            self.loc = new_loc


class Game():

    def __init__(self, tile_list):
        self.tiles = tiles_to_dict(tile_list)
        self.ball = Ball(loc=[loc for loc, val in self.tiles.items() if val == 4][0])
        self.tile_loc = [loc for loc, val in self.tiles.items() if val == 3][0]

    def count_blocks(self):
        nblocks = 0
        for val in self.tiles.values():
            if val == 2:
                nblocks += 1
            return nblocks

    def return_gamestate(self):
            ymin = min([l[1] for l in self.tiles.keys()])
            xmin = min([l[0] for l in self.tiles.keys()])
            ymax = max([l[1] for l in self.tiles.keys()])
            xmax = max([l[0] for l in self.tiles.keys()])

            gs = np.zeros((ymax+1-ymin, xmax+1-xmin))
            for loc, val in self.tiles.items():
                gs[loc[1], loc[0]] = val

            return(gs)

    def plot_gamestate(self, outputfn=None):
            colors = ['black', 'gray', 'blue', 'green', 'red']
            fig = plt.figure()
            plt.imshow(self.return_gamestate(),
                       cmap=mpl.colors.ListedColormap(colors))
            if outputfn:
                plt.savefig(outputfn+'.png')

            return fig

    def cmdline_plot(self):
            print_dict = {0: ' ',
                          1: 'X',
                          2: 'B',
                          3: '-',
                          4: 'o'}
            gs = self.return_gamestate()
            output_arr = np.vectorize(print_dict.get)(gs)
            for row in output_arr:
                print(''.join(row))


def tiles_to_dict(tile_list):
    tile_dict = {}
    for t in tile_list:
        tile_dict[(t[0], t[1])] = t[2]
    return tile_dict


print('Part A')
fn = '13.txt'
program = ic.input_to_program(fn)
input_val = 0
c = ic.Computer(program, input_val)

tiles = []
output_counters = cycle(range(3))
output_counter = next(output_counters)
while c.opcode != 99:
    c.run_op(verbose=False)
    if c.opcode == 4:
        if output_counter == 0:
            tile = [c.output_val]
            # output_counter = next(output_counters)
        elif output_counter == 1:
            tile.append(c.output_val)
            # output_counter = next(output_counters)
        elif output_counter == 2:
            tile.append(c.output_val)
            tiles.append(tile)
        output_counter = next(output_counters)

g_init = Game(tiles)
print('No. blocks: {}'.format(g_init.count_blocks()))

print('\nPart B')
g_init.plot_gamestate('game_imgs/init.png')
scores = dict()


# Tkinter game
# root= tk.Tk()
with open('game_inputs.txt', 'r') as fh:
    good_inputs = fh.readline().rstrip().split(',')
good_inputs = good_inputs[:-60]

target_locs = {}
usr_inputs = []
for run_no in range(1):
    fn = '13.txt'
    program = ic.input_to_program(fn)
    input_val = 0
    c = ic.Computer(program, input_val)
    c.program[0] = 2  # Insert coins

    g = deepcopy(g_init)


    output_counters = cycle(range(3))
    output_counter = next(output_counters)
    scores[run_no] = []

    time = 0
    prev_tile_time = -1

    while c.opcode != 99:
        c.run_op()
        if c.opcode == 4:
            if output_counter == 0:
                tile = [c.output_val]
            elif output_counter == 1:
                tile.append(c.output_val)
            elif output_counter == 2:
                if tile == [-1, 0]:
                    scores[run_no].append(c.output_val)
                else:
                    g.tiles[tuple(tile)] = c.output_val  # update tiles
                    if c.output_val == 4:
                        # Ball moves
                        new_loc = tuple(tile)
                        g.ball.update_loc(new_loc)

                        # Check if ball going out next move
                        if g.ball.loc[1] + g.ball.direction[1] == g.tile_loc[1] - 1:
                            next_tile_time = time + 2
                            for t in range(prev_tile_time+1, next_tile_time):
                                target_locs[t] = g.ball.loc[0] + g.ball.direction[0]
                            prev_tile_time = next_tile_time
                            print('going out')
                    if c.output_val == 3:
                        # Tile moves
                        g.tile_loc = tuple(tile)
                    if c.output_val in [3, 4]:
                        # if time+1 in target_locs:
                        #       c.input_val = np.sign(target_locs[time+1] - g.tile_loc[0])
                        # else:
                        #       c.input_val = 0
                        time += 1
                        # g.plot_gamestate()
                        # im = g.update_plot(im)
                        input_dict = {'a': -1, 's': 0, 'd': 1}
                        if good_inputs:
                            uinput = good_inputs.pop(0)
                        else:
                            g.cmdline_plot()
                            uinput = input()
                        usr_inputs.append(uinput)
                        if uinput not in input_dict:
                            None
                        else:
                            c.input_val = input_dict[uinput]
                        print(scores)
                output_counter = next(output_counters)

print(scores)
with open('game_inputs.txt', 'w') as fh:
    fh.write(','.join(usr_inputs))
