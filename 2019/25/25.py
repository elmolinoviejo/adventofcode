import sys
import networkx as nx
from itertools import combinations
sys.path.append('../')
import intcode2019 as ic

# Movement via north, south, east, or west. To take an item the droid sees in
# the environment, use the command take <name of item>. For example, if the
# droid reports seeing a red ball, you can pick it up with take red ball. To
# drop an item the droid is carrying, use the command drop <name of item>. For
# example, if the droid is carrying a green ball, you can drop it with drop
# green ball. To get a list of all of the items the droid is currently
# carrying, use the command inv (for "inventory").


# class Map:
#     def __init__(self):
#         self.locs = []
#         self.graph = nx.Graph()


# class MapLoc:
#     def __init__(self, loc_number):
#         self.number = loc_number
#         self.items = []
#         self.text = ''
#         self.neighbors = []

#     def __str__(self):
#         return self.text[:10]

#     def __repr__(self):
#         return self.number


def get_input():
    str_input = input()
    input_ascii = [int(ord(x)) for x in str_input]
    input_ascii.append(int(10))
    return input_ascii, str_input


def get_commands(fn):
    with open(fn, 'r') as fh:
        commands = []
        for l in fh:
            commands.append(l)
    return commands


print('Part A')
fn = '25.txt'
program = ic.input_to_program(fn)
c = ic.Computer(program)

output_ascii = []
commands = []
commands = get_commands('25_cmds1.txt')
# print(commands)

# permutate items
all_items = [
    'tambourine', #
    'hologram',
    'fuel cell', #
    'wreath', #
    'boulder', #
    'fixed point', #
    'manifold', #
    'polygon'] #


right_items = [
    ('boulder',
     'fixed point',
     'manifold',
     'polygon')]

item_combinations = right_items

# item_combinations = []
# for n_items in range(len(all_items)):
#     if n_items == 0:
#         continue
#     item_combinations.extend(combinations(all_items, n_items))



item_results = {}

prior_output = None
print_switch = False
with open('25_outputs.txt', 'w') as fh:

    while item_combinations:
        run_comp = True
        items = item_combinations.pop(0)
        commands.extend(['take ' + item + '\n' for item in items])
        # commands.append('north\n')
        # commands.extend(['drop ' + item + '\n' for item in items])

        # fh.write(', '.join([x for x in items]))

        # [print(com) for com in commands]
        while run_comp:
            # fh.write(chr(c.output_val))
        # while False:
            # while c.opcode != 99:
            # if 'anta' in ''.join([chr(a) for a in output_ascii]):
            #     print(''.join([chr(a) for a in output_ascii]))
            #     print(items)
            c.run_op()
            if c.opcode == 4:
                output_ascii.append(c.output_val)
                if print_switch:
                    print(''.join([chr(a) for a in output_ascii]))
                if (prior_output, c.output_val) == (100, 63):
                    output_string = ''.join([chr(a) for a in output_ascii])
                    # fh.write(output_string)
                    # if 'Pressure-Sensitive' in output_string:
                    #     print(items)
                    #     print(output_string)
                    print(''.join([chr(a) for a in output_ascii]))
                    output_ascii = []
                    if commands:
                        # print(len(commands))
                        str_input = commands.pop(0)
                        input_ascii = [int(ord(x)) for x in str_input]
                        # print(input_ascii)
                    else:
                        # item_results[items] = output_string
                        # run_comp = False
                        # break
                        input_ascii, str_input = get_input()
                        print_switch = True
                    c.input_val = input_ascii.pop(0)
                prior_output = c.output_val
            if c.opcode == 3:
                if input_ascii:
                    c.input_val = input_ascii.pop(0)

# print(item_results)
