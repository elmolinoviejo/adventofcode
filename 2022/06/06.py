def read_input(fn):
    with open(fn, 'r') as fh:
        return fh.read()

def find_first_unique(msg, subset_size):
    for ind in range(subset_size, len(msg)):
        subset = msg[ind - subset_size:ind]
        if len(set(subset)) == subset_size:
            return ind

msg = read_input('06.txt')
print('Part 1')
subset_size = 4
print(find_first_unique(msg, subset_size))
print('Part 2')
subset_size = 14
print(find_first_unique(msg, subset_size))
