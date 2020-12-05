def input_to_bps(fn):
    bps = []
    with open(fn) as fh:
        for line in fh:
            bps.append(line.rstrip())
    return bps


def bp_to_seat(bp):
    # [row, col]
    row_bp = bp[:8]
    col_bp = bp[7:]

    row = 0
    for r_iter, r_val in enumerate(row_bp):
        if r_val == 'B':
            row += 128 / (2 ** (r_iter + 1))

    col = 0
    for c_iter, c_val in enumerate(col_bp):
        if c_val == 'R':
            col += 8 / (2 ** (c_iter + 1))

    return ([int(row), int(col)])


def seat_id(seat_coord):
    return 8 * seat_coord[0] + seat_coord[1]


bps = input_to_bps('05.txt')
# Part 1
seat_coords = []
seat_ids = []
for bp in bps:
    seat_coords.append(bp_to_seat(bp))
    seat_ids.append(seat_id(bp_to_seat(bp)))
print(f"Part A:\t{max(seat_ids)}")

# Part 2
for row in range(1, 127):
    for col in range(0, 8):
        if [row, col] not in seat_coords:
            val = seat_id([row, col])
            if (val + 1 in seat_ids) and (val - 1 in seat_ids):
                print(f"Part B:\t{val}")
