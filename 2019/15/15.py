import sys
import networkx as nx
import numpy as np
sys.path.append('../')
import intcode2019 as ic


def initialize_computer(fn):
    program = ic.input_to_program(fn)
    c = ic.Computer(program)
    return c


def run_move(computer, input_val):
    computer.input_val = input_val
    while computer.opcode != 4:
        computer.run_op()
    computer.opcode = None
    return computer.output_val


def wall_follow_to_end(c, start_loc=(0, 0), move_dir=1):
    wall_locs = []
    passage_locs = [start_loc]
    g = nx.Graph()
    g.add_node(start_loc)
    left_turns = dict(zip([1, 2, 3, 4],
                          [3, 4, 2, 1]))
    right_turns = {y: x for x, y in left_turns.items()}
    loc_changes = {1: (0, -1),
                   2: (0, 1),
                   3: (-1, 0),
                   4: (1, 0)}

    current_loc = start_loc
    end_cond = False
    while not end_cond:
        input_val = move_dir
        next_loc = (current_loc[0] + loc_changes[move_dir][0],
                    current_loc[1] + loc_changes[move_dir][1])
        output_val = run_move(c, input_val)

        if output_val in [1, 2]:
            # move to that location and update graph and passages
            g.add_edge(current_loc, next_loc)
            if next_loc not in passage_locs:
                passage_locs.append(next_loc)
            # then try a right turn next
            move_dir = right_turns[move_dir]
        elif output_val == 0:
            # if hit a wall, make a left turn
            move_dir = left_turns[move_dir]
            if next_loc not in wall_locs:
                wall_locs.append(next_loc)
            next_loc = current_loc
        current_loc = next_loc
        if output_val == 2:
            end_cond = True
            end_loc = current_loc

    return g, passage_locs, wall_locs, start_loc, end_loc


def explore_shortest_path(g, passage_locs, wall_locs, shortest_path):
    # Move along shortest path, if any adjacent spaces are unkown
    # move into it
    # Return new updated graph and locations
    loc_changes = {1: (0, -1),
                   2: (0, 1),
                   3: (-1, 0),
                   4: (1, 0)}
    end_found = False
    new_passages = []
    for path_ind, current_loc in enumerate(shortest_path):
        # Try adjacent spaces
        for move_dir, loc_change in loc_changes.items():
            next_loc = (current_loc[0] + loc_change[0],
                        current_loc[1] + loc_change[1])
            # Try unkown spaces
            if next_loc not in passage_locs + wall_locs:
                output_val = run_move(c, move_dir)

                if output_val == 1:
                    # move to that location and
                    # return updated graph and passages
                    new_passages.append(next_loc)
                    g.add_edge(current_loc, next_loc)
                    passage_locs.append(next_loc)
                    return g, passage_locs, wall_locs, end_found, new_passages
                elif output_val == 0:
                    # if hit a wall, record and try the next space
                    wall_locs.append(next_loc)
                    if path_ind < len(shortest_path) - 1:
                        continue
                        # next_loc = shortest_path[path_ind + 1]
                        # move_coord = (next_loc[0] - current_loc[0],
                        #               next_loc[1] - current_loc[1])
                        # move_dir = [d for d, coord in loc_changes.items()
                        #             if coord == move_coord][0]
                        # output_val = run_move(c, move_dir)
                    else:
                        end_found = True
                        return g, passage_locs, wall_locs, end_found, new_passages
                    continue

                if output_val == 2:
                    end_found = True
                    return g, passage_locs, wall_locs, end_found, new_passages
            else:
                continue
        # Move to next location along the shortest path
        try:
            next_loc = shortest_path[path_ind + 1]
        except IndexError:
            return g, passage_locs, wall_locs, end_found, new_passages
        move_coord = (next_loc[0] - current_loc[0],
                      next_loc[1] - current_loc[1])
        move_dir = [d for d, coord in loc_changes.items()
                    if coord == move_coord][0]
        output_val = run_move(c, move_dir)

    return g, passage_locs, wall_locs, end_found, new_passages


def plot_map(passage_locs, wall_locs, o2_locs=[],
             end_loc=None, start_loc=(0, 0)):
    minx = min([min([x for x, y in passage_locs]),
                min([x for x, y in wall_locs])])
    maxx = max([max([x for x, y in passage_locs]),
                max([x for x, y in wall_locs])])
    miny = min([min([y for x, y in passage_locs]),
                min([y for x, y in wall_locs])])
    maxy = max([max([y for x, y in passage_locs]),
                max([y for x, y in wall_locs])])
    map_str = ''
    for y in np.arange(miny, maxy + 1):
        for x in np.arange(minx, maxx + 1):
            if end_loc and (x, y) == end_loc:
                map_str += 'O'
            elif (x, y) == start_loc:
                map_str += '@'
            elif (x, y) in passage_locs:
                map_str += '.'
            elif (x, y) in wall_locs:
                map_str += '#'
            elif (x, y) in o2_locs:
                map_str += 'O'
            else:
                map_str += '?'
        map_str += '\n'
    print(map_str)
    return map_str


def get_dirs_from_end_loc(g, end_loc, start_loc=(0, 0)):
    loc_changes = {1: (0, -1),
                   2: (0, 1),
                   3: (-1, 0),
                   4: (1, 0)}
    dir_order = []
    path = nx.shortest_path(g, start_loc, end_loc)
    for ind, loc in enumerate(path):
        if ind < len(path) - 1:
            delta = (path[ind + 1][0] - loc[0],
                     path[ind + 1][1] - loc[1])
            move_dir = [d for d, change in loc_changes.items()
                        if change == delta][0]
            dir_order.append(move_dir)
    return dir_order


def locs_to_check(passage_locs, wall_locs, locs_to_check):
    loc_changes = {1: (0, -1),
                   2: (0, 1),
                   3: (-1, 0),
                   4: (1, 0)}
    all_check_locs = []
    for ploc in locs_to_check:
        check_locs = []
        for move_dir, loc_change in loc_changes.items():
            next_loc = (ploc[0] + loc_change[0],
                        ploc[1] + loc_change[1])
            if next_loc not in passage_locs + wall_locs:
                check_locs.append(next_loc)
        if len(check_locs) > 0:
            # all_check_locs[ploc] = check_locs
            all_check_locs.append(ploc)
    return all_check_locs


def fill_o2(g, passage_locs, o2_locs):
    loc_changes = {1: (0, -1),
                   2: (0, 1),
                   3: (-1, 0),
                   4: (1, 0)}
    locs_to_fill = []
    for o2_loc in o2_locs:
        for delta in loc_changes.values():
            adj = (o2_loc[0] + delta[0],
                   o2_loc[1] + delta[1])
            # print(adj)
            if adj in passage_locs:
                locs_to_fill.append(adj)
    for loc in list(set(locs_to_fill)):
        passage_locs.remove(loc)
        o2_locs.append(loc)
    return passage_locs, o2_locs


print('Part A')
fn = '15.txt'
# Find end location
c = initialize_computer(fn)
g, passage_locs, wall_locs, start_loc, end_loc = wall_follow_to_end(c)
shortest_path = nx.shortest_path(g, start_loc, end_loc)
# plot_map(passage_locs, wall_locs, end_loc)
print(len(shortest_path) - 1)


print('Part B')
# Make a list of passages that have unknown adjacent locations
# plot_map(passage_locs, wall_locs, end_loc)
# plot_map(passage_locs, wall_locs, end_loc)
check_locs = locs_to_check(passage_locs, wall_locs, passage_locs)
n_iter = 0
while len(check_locs) > 0:
    check_loc = check_locs.pop(0)
    c = initialize_computer(fn)
    shortest_path = nx.shortest_path(g, (0, 0), check_loc)
    g, passage_locs, wall_locs, end_found, new_passages = explore_shortest_path(
        g, passage_locs, wall_locs, shortest_path)
    check_locs.extend(locs_to_check(passage_locs, wall_locs, new_passages))
    # print(check_locs)
    if len(check_locs) == 0:
        check_locs = locs_to_check(passage_locs, wall_locs, passage_locs)
    n_iter += 1
    # if n_iter % 25 == 0:
    #     plot_map(passage_locs, wall_locs)
    plot_map(passage_locs, wall_locs)
# print(locs_to_check(passage_locs, wall_locs, passage_locs))

passage_locs.remove(end_loc)
passage_locs.append(start_loc)
o2_locs = [end_loc]
# for _ in range(10):
ans = 0
plot_map(passage_locs, wall_locs, o2_locs=o2_locs)
# for _ in range(10):
while passage_locs:
    passage_locs, o2_locs = fill_o2(g, passage_locs, o2_locs)
    ans += 1
    print(ans)
    plot_map(passage_locs, wall_locs, o2_locs=o2_locs)

# 136 and 137 and 138 are too low
