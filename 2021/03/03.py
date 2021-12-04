from collections import Counter


def read_input(fn):
    inputs = []
    with open(fn) as fh:
        for line in fh.readlines():
            inputs.append(line.rstrip())
    return inputs


def count_positions(nums):
    pos = [''.join(n) for n in zip(*nums)]
    counts = []
    for col in pos:
        counts.append(Counter(col))
    return counts


def get_gas_val(inputs, gas):
    bit_ind = 0
    while bit_ind < 12:
        if len(inputs) == 1:
            return inputs[0]
        counts = count_positions(inputs)
        common = counts[bit_ind].most_common()
        if common[0][1] == common[1][1]:
            mc = '1'
            lc = '0'
        else:
            mc = common[0][0]
            lc = common[1][0]
        if gas == 'o2':
            inputs = [n for n in inputs if n[bit_ind] == mc]
        elif gas == 'co2':
            inputs = [n for n in inputs if n[bit_ind] == lc]
        bit_ind += 1
    return inputs[0]


# Part One
fn = '03.txt'
inputs = read_input(fn)
counts = count_positions(inputs)
g, e = '', ''
for c in counts:
    common = c.most_common()
    g += common[0][0]
    e += common[1][0]
print(int(g, 2) * int(e, 2))

# Part Two
inputs = read_input(fn)
o2 = get_gas_val(inputs, 'o2')
inputs = read_input(fn)
co2 = get_gas_val(inputs, 'co2')

print(int(o2, 2) * int(co2, 2))
