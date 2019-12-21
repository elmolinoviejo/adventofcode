import sys
import networkx as nx
sys.path.append('../')
import intcode2019 as ic


def move_bot(computer, input_val):
    computer.input_val = input_val
    while computer.opcode != 4:
        computer.run_op()
    computer.opcode = None
    return computer.output_val

print('Part A')
fn = '15.txt'
program = ic.input_to_program(fn)
c = ic.Computer(program)

# Inputs:
 # 1, N
 # 2, S
 # 3, W
 # 4, E

# Outputs
# 0: hit a wall, no position change
# 1: moved one step
# 2: moved one step and found O2 system


# Go until you hit a wall
# move left
# keep trying to move into the wall
# if you cant, update wall_loc and move left
# if you can, update direction and continue to follow the wall

start_loc = (0, 0)
wall_locs = []
passage_locs = [(0, 0)]
g =nx.Graph()
g.add_node(start_loc)
left_turns = dict(zip([1, 2, 3, 4],
                      [3, 4, 2, 1]))
loc_changes = {1: (-1, 0),
               2: (1, 0),
               3: (-1, 0),
               4: (1, 0)}


move_dir = 1
current_loc = start_loc
end_cond = False
# while not end_cond:
for _ in range(1):
    input_val = move_dir
    output_val = move_bot(c, input_val)
    next_loc = (current_loc[0] + loc_changes[move_dir][0],
                current_loc[1] + loc_changes[move_dir][1])
    if output_val in [1, 2]:
        g.add_edge(current_loc, next_loc)
        passage_locs.append(next_loc)

    elif output_val == 0:
        move_dir = left_turns[move_dir]
        wall_locs.append(next_loc)
    current_loc = next_loc
    if output_val == 2:
        end_cond = True
        end_loc = current_loc
    if output

print(output_val)
