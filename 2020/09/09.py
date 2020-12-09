def get_num_list(fn):
    num_list = [int(g) for g in open(fn).read().split('\n')]
    return num_list


def partA(num_list):
    for ind, n in enumerate(num_list):
        if ind < 25:
            continue
        prev = num_list[ind - 25:ind]
        num_ok = False
        for n2 in prev:
            if n - n2 != n2:
                if n - n2 in prev:
                    num_ok = True
                    break
        if not num_ok:
            return n


def partB(num_list):
    target = partA(num_list)
    for ind in range(len(num_list)):
        for len_sublist in range(len(num_list) - ind):
            sublist = num_list[ind:ind + len_sublist]
            if sum(sublist) == target:
                return min(sublist) + max(sublist)
            elif sum(sublist) > target:
                break


fn = '09.txt'
num_list = get_num_list(fn)

print(f"Part A:\t{partA(num_list)}")
print(f"Part B:\t{partB(num_list)}")
