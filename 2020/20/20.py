import numpy as np
import networkx as nx


def load_tiles(fn):
    raw_tiles = [g for g in open(fn).read().split('\n\n')]
    tiles = {}
    for tile in raw_tiles:
        tile = tile.split('\n')

        tn = tile[0].split('Tile ')[1][:-1]
        tiles[tn] = np.chararray([10, 10], unicode=True)
        for y, vals in enumerate(tile[1:]):
            for x, val in enumerate(vals):
                tiles[tn][y][x] = val

    return tiles


def rotflip(arr, rf):
    rot, flip = rf
    arr = np.rot90(arr, rot)
    for f in range(flip):
        arr = np.flip(arr, axis=1)
    return arr


def rotflip_rev(arr, rf):
    rot, flip = rf
    for f in range(flip):
        arr = np.flip(arr, axis=1)
    arr = np.rot90(arr, 4 - (rot % 4))
    return arr


def get_edge_strs(tiles):
    edge_strs = {}

    for tn, tile in tiles.items():
        for r in range(4):
            for f in range(2):
                temp_tile = rotflip(tile, (r, f))
                es = ''.join(temp_tile[0])  # top string
                if es not in edge_strs:
                    edge_strs[es] = []
                edge_strs[es].append((tn, (r, f)))
    return edge_strs  # str: tile_num, (edge_num, flip)


def make_graph(tiles, edge_strs):
    G = nx.Graph()
    for m in edge_strs.values():
        if len(m) > 1:
            n1, rf1 = m[0]
            n2, rf2 = m[1]
            if not G.has_edge(n1, n2):
                G.add_edge(n1, n2, o={n1: rf1, n2: rf2})
    return G


def place_tiles(G, tiles, tile_locs, start):
    rel_tile_locs = {0: (-1, 0),
                     1: (0, 1),
                     2: (1, 0),
                     3: (0, -1)}
    match_edge = {(0, 0): []}

    tile_locs[(0, 0)] = start
    queue = [start]
    while len(queue) > 0:
        t1 = queue.pop()
        # t2 is placed neighbor
        for t2 in G.neighbors(t1):
            if t2 not in tile_locs.values():
                queue.append(t2)
        if t1 in tile_locs.values():
            continue
        else:
            # find placed neighbor
            t2 = [x for x in G.neighbors(t1) if x in tile_locs.values()][0]
            edge_o = G.edges[t1, t2]['o']
            o1, o2 = [edge_o[x] for x in [t1, t2]]

            # place new tile
            rel_loc = rel_tile_locs[(o2[0])]
            placed_loc = [k for k, v in tile_locs.items() if v == t2][0]
            new_loc = tuple([v + diff for v, diff in zip(placed_loc, rel_loc)])
            if new_loc in tile_locs:
                print(f'###OVERWRITE###\t{new_loc}\t{t1}')
            tile_locs[new_loc] = t1

            # get matched edge
            # reverse needed rotflip so that top edge of t2 is the match
            temp_tile = rotflip(tiles[t2], (o2[0], o2[1]))
            match_edge = ''.join(temp_tile[0])  # top string
            # spin and flip new tile so that bottom edge of t1 is the match
            for r in range(4):
                for f in range(2):
                    temp_tile = rotflip(tiles[t1], (r, f))
                    es = ''.join(temp_tile[9])  # bottom string
                    if es == match_edge:
                        rf = (r, f)
                        break

            updated_tile = tiles[t1]
            updated_tile = rotflip(updated_tile, rf)
            updated_tile = rotflip_rev(updated_tile, (o2[0], o2[1]))
            tiles[t1] = updated_tile

            # remake graph with flipped tile
            edge_strs = get_edge_strs(tiles)
            G = make_graph(tiles, edge_strs)
    return G, tiles, tile_locs


def combine_tiles(tiles, tile_locs, edge_length=10):
    out_arr = np.chararray([12 * edge_length, 12 * edge_length], unicode=True)
    out_arr.fill('x')
    # align edges to top left
    miny = min(y for y, x in tile_locs.keys())
    minx = min(x for y, x in tile_locs.keys())
    # edge buffer
    for tl, tile_n in tile_locs.items():
        tile_arr = tiles[tile_n]
        # adjust loc
        ty, tx = tl
        ty, tx = (ty - miny) * edge_length, (tx - minx) * edge_length
        # adjust input arr to edge_length
        eb = int(((len(tile_arr) - edge_length) / 2))
        tile_arr = tile_arr[eb:eb + edge_length, eb:eb + edge_length]
        out_arr[ty:ty + edge_length, tx:tx + edge_length] = tile_arr
    return(out_arr)


def tile_str(arr):
    out = ''
    for line in arr:
        # print(line)
        out += ''.join(line)
        out += '\n'
    out = out.replace('x', ' ')
    return out


tiles = load_tiles('20.txt')
edge_strs = get_edge_strs(tiles)
G = make_graph(tiles, edge_strs)

# Part 1
corners = []
ans = 1
for n in G:
    if len(G[n]) == 2:
        corners.append(n)
        ans *= int(n)
print(f"Part 1:\t{ans}")

# Part 2
start = corners[0]  # one of the corners
tile_locs = {}  # (y, x): tile
G, tiles, tile_locs = place_tiles(G, tiles, tile_locs, start)
# print(tile_locs)
out_arr = combine_tiles(tiles, tile_locs, edge_length=8)
out_str = tile_str(out_arr)
with open('test_out.txt', 'w') as fh:
    fh.write(out_str)

sm_match_locs = [(0, 18),
                 (1, 0), (1, 5), (1, 6), (1, 11),
                 (1, 12), (1, 17), (1, 18), (1, 19),
                 (2, 1), (2, 4), (2, 7), (2, 10),
                 (2, 13), (2, 16)]

ans_list = []
for r in range(4):
    for f in range(2):
        xx = np.rot90(out_arr, r)
        xx = np.flip(xx, axis=1)

        ans = 0
        for y in range(76):
            for x in range(93):
                start_loc = (y, x)
                match = False
                locs = [(y + sm[1], x + sm[0]) for sm in sm_match_locs]
                vals = [xx[loc] for loc in locs]
                if all([x == '#' for x in vals]):
                    ans += 1
        ans_list.append(ans)

num = len([s for s in out_str if s == '#'])
ans = num - max(ans_list) * 15
print(f"Part 2:\t{ans}")
