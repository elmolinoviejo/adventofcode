def read_input(fn):
    inputs = []
    with open(fn) as fh:
        for line in fh.readlines():
            inputs.append(int(line.rstrip()))
    return inputs


def compare_adj_depths(depth_list):
    count = 0
    prev_d = 0
    for ind, d in enumerate(depth_list):
        if ind < 1:
            continue
        if d > prev_d:
            count += 1
        prev_d = d
    return count


def compare_step_depths(depth_list, step):
    count = 0
    prev_sum = 0
    for ind, d in enumerate(depth_list):
        if ind < step:
            continue
        # inds = [ind - x for x in range(step)]
        d_sum = sum(depth_list[ind - step:ind])
        if d_sum > prev_sum:
            count += 1
        prev_sum = d_sum
    return count


depth_list = read_input('01.txt')
# Part One
print(compare_adj_depths(depth_list))

# Part Two
print(compare_step_depths(depth_list, step=3))
