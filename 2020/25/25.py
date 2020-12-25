def handshake(val, subjectnum, loopsize):
    for _ in range(loopsize):
        val = subjectnum * val
        val = val % 20201227
    return val

# input
cpk = 15335876
dpk = 15086442

val = 1
loopsize = 1
while True:
    val = handshake(val, 7, 1)
    if val == cpk:
        next_loopsize = loopsize
        next_input = dpk
        break
    elif val == dpk:
        next_loopsize = loopsize
        next_input = cpk
        break
    loopsize += 1

ans = handshake(1, next_input, next_loopsize)
print(f"Part 1:\t{ans}")
