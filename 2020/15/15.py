def step(n, ind, nd):
    if n not in nd:
        nd[n] = []
    # print(n, nd[n])
    if len(nd[n]) < 2:
        next_num = 0
    else:
        next_num = nd[n][-1] - nd[n][-2]
    if next_num not in nd:
        nd[next_num] = []
    nd[next_num].append(ind)
    ind += 1
    n = next_num
    return n, ind, nd


nums = '18,11,9,0,5,1'
nums = [int(x) for x in nums.split(',')]
nd = {n: [ind] for ind, n in enumerate(nums)}
n = nums[-1]
ind = len(nums)

for _ in range(30000000):
    n, ind, nd = step(n, ind, nd)
    if ind == 2020:
        print(f"Part 1:\t{n}")
    if ind == 30000000:
        print(f"Part 2:\t{n}")
        break
