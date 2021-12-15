def load_input(fn):
    pis = {}
    with open(fn) as fh:
        temp, plist = fh.read().split('\n\n')
        for p in plist.split('\n'):
            p1, p2 = p.split(' -> ')
            pis[p1] = p2
#             pis.append(tuple(p.split(' -> ')))
    return temp, pis


def step(temp, pis):
    new_temp = []
    for ind, c in enumerate(temp):
        if ind==len(temp) - 1:
            continue
        pair = c + temp[ind+1]
        new_temp.append(c)
        if pair in pis:
            new_temp.append(pis[pair])
#         print(new_temp)
    new_temp.append(temp[-1])
#             to_add.append(tuple([pis[pair], ind]))
#     print(to_add)
    
#     new_temp = ''
#     ind_base = 1
#     for ind, 
    return ''.join(new_temp)

day = '14'
fn = f'../{day}/{day}.txt'
# fn = f'../{day}/{day}_test.txt'
# fn = f'../{day}/{day}_test2.txt'

temp, pis = load_input(fn)

for _ in range(10):
    temp = step(temp, pis)

x = Counter(temp)
print(x.most_common())