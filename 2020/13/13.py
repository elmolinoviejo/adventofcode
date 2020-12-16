def get_buslist(fn):
    lines = [g for g in open(fn).read().split('\n')]
    start_time = int(lines[0])
    buslist = lines[1].split(',')
    # buslist = [int(b) for b in buslist if b != 'x']
    return start_time, buslist


def part1(busmap, start_time, step=1):
    time = start_time
    while True:
        for bi in busmap.values():
            if time % bi == 0:
                return bi, time
        time += step


def find_first_mults(bi_ind, bid, step, start=0):
    time = step + start
    times = []
    while True:
        if (time + bi_ind) % bid == 0:
            times.append(time)
            if len(times) > 1:
                return times
        time += step


def part2(busmap, step_init, start=0):
    step = step_init
    for bi_ind, bid in busmap.items():
        times = find_first_mults(bi_ind, bid, step, start)
        if True:
            step = times[1] - times[0]
            start = times[0]

    return times[0]


start_time, buslist = get_buslist('13.txt')
busmap = {ind: int(bi) for ind, bi in enumerate(buslist) if bi != 'x'}
bi1, time1 = part1(busmap, start_time)

print(f"Part 1:\t{bi1 * (time1 - start_time)}")
print(f"Part 2:\t{part2(busmap, 1)}")
