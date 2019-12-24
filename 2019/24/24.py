import numpy as np

class Eris():
    def __init__(self):
        self.spaces = dict()
        for x in range(5):
            for y in range(5):
                self.spaces[(x, y)] = Space()

    def read_spaces_from_file(self, fn):
        with open(fn, 'r') as fh:
            for y, l in enumerate(fh):
                for x, s in enumerate(l.rstrip()):
                    if s == '.':
                        alive = False
                    elif s == '#':
                        alive = True
                    self.spaces[(x, y)].alive = alive

    def fill_neighbors(self):
        for (x, y), space in self.spaces.items():
            for neighbor in [(x + 1, y), (x - 1, y),
                             (x, y + 1), (x, y - 1)]:
                if neighbor in self.spaces:
                    space.neighbors.append(neighbor)

    def space_hash(self):
        space_hash = ''
        for y in range(5):
            for x in range(5):
                if self.spaces[(x, y)].alive:
                    space_hash += '#'
                else:
                    space_hash += '.'
            # space_hash += '\n'
        return space_hash

    def pass_minute(self):
        new_alive_states = dict()
        for sloc, space in self.spaces.items():
            n_alive, n_empty = 0, 0
            for n in space.neighbors:
                if self.spaces[n].alive:
                    n_alive += 1
                else:
                    n_empty += 1
            if space.alive:
                if n_alive != 1:
                    new_alive_states[sloc] = False
                else:
                    new_alive_states[sloc] = True
            elif not space.alive:
                if n_alive in [1, 2]:
                    new_alive_states[sloc] = True
                else:
                    new_alive_states[sloc] = False
        for sloc, state in new_alive_states.items():
            self.spaces[sloc].alive = state

class Eris3D():
    def __init__(self):
        self.spaces = dict()
        for x in range(5):
            for y in range(5):
                if (x, y) == (2, 2):
                    continue
                else:
                    self.spaces[(x, y, 0)] = Space(recursive=True)

    def read_spaces_from_file(self, fn):
        with open(fn, 'r') as fh:
            for y, l in enumerate(fh):
                for x, s in enumerate(l.rstrip()):
                    if (x, y) == (2, 2):
                        continue
                    if s == '.':
                        alive = False
                    elif s == '#':
                        alive = True
                    self.spaces[(x, y, 0)].alive = alive

    def fill_neighbors(self):
        for (x, y, z), space in self.spaces.items():
            neighbor_list = [(x + 1, y, z), (x - 1, y, z),
                             (x, y + 1, z), (x, y - 1, z)]
            if x == 0:
                neighbor_list.append((1, 2, z - 1))
            elif x == 4:
                neighbor_list.append((3, 2, z - 1))
            if y == 0:
                neighbor_list.append((2, 1, z - 1))
            elif y == 4:
                neighbor_list.append((2, 3, z - 1))

            if (x, y) == (2, 1):
                neighbor_list.extend([(x, 0, z + 1) for x in range(5)])
            if (x, y) == (2, 3):
                neighbor_list.extend([(x, 4, z + 1) for x in range(5)])
            if (x, y) == (1, 2):
                neighbor_list.extend([(0, y, z + 1) for y in range(5)])
            if (x, y) == (3, 2):
                neighbor_list.extend([(4, y, z + 1) for y in range(5)])

            if (2, 2, z) in neighbor_list:
                neighbor_list.remove((2, 2, z))

            for neighbor in neighbor_list:
                if neighbor[0] < 0 or neighbor[1] < 0:
                    continue
                elif neighbor[0] > 4 or neighbor[1] > 4:
                    continue
                else:
                    space.neighbors.add(neighbor)

    def space_hash(self, z_vals=False):
        space_hash = ''
        minz = min([z for x, y, z in self.spaces.keys()])
        maxz = max([z for x, y, z in self.spaces.keys()])
        if not z_vals:
            z_vals = np.arange(minz, maxz + 1)
        space_hash += '-----\n\n'
        for z in z_vals:
            for y in range(5):
                for x in range(5):
                    if (x, y, z) not in self.spaces:
                        space_hash += ' '
                    elif self.spaces[(x, y, z)].alive:
                        space_hash += '#'
                    else:
                        space_hash += '.'
                space_hash += '\n'
            space_hash += f'Level {z}\n\n'
        return space_hash

    def add_new_neighbors(self):
        new_spaces = []
        for sloc, space in self.spaces.items():
            for n in space.neighbors:
                if n not in self.spaces:
                    new_spaces.append(n)
        for s in new_spaces:
            self.spaces[s] = Space(recursive=True)

    def pass_minute(self):
        new_alive_states = dict()
        for sloc, space in self.spaces.items():
            n_alive, n_empty = 0, 0
            for n in space.neighbors:
                if n in self.spaces:
                    if self.spaces[n].alive:
                        n_alive += 1
                    else:
                        n_empty += 1
                else:
                    n_empty += 1
            if space.alive:
                if n_alive != 1:
                    new_alive_states[sloc] = False
                else:
                    new_alive_states[sloc] = True
            elif not space.alive:
                if n_alive in [1, 2]:
                    new_alive_states[sloc] = True
                else:
                    new_alive_states[sloc] = False
        for sloc, state in new_alive_states.items():
            self.spaces[sloc].alive = state

    def count_bugs(self):
        n_bugs = 0
        for space in self.spaces.values():
            if space.alive:
                n_bugs += 1
        return n_bugs


class Space:
    def __init__(self, recursive=False):
        self.alive = False
        if recursive:
            self.neighbors = set()
        else:
            self.neighbors = []


print('Part A')
eris = Eris()
eris.read_spaces_from_file('24.txt')
eris.fill_neighbors()

hashes = set()
end_cond = False
while not end_cond:
    eris.pass_minute()
    shash = eris.space_hash()
    if shash in hashes:
        end_cond = True
        final_hash = shash
    else:
        hashes.add(shash)

ans = 0
for ind, s in enumerate(final_hash):
    if s == '#':
        ans += (2 ** ind)
print(ans)

print('Part B')
eris = Eris3D()
eris.read_spaces_from_file('24.txt')
eris.fill_neighbors()
for _ in range(200):
    eris.add_new_neighbors()
    eris.fill_neighbors()
    eris.pass_minute()

print(eris.count_bugs())
