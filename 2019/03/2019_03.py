import numpy as np

def file_to_wire_directions(fn):
    w1, w2 = [], []
    with open(fn) as fh:
        w1 = fh.readline().rstrip().split(',')
        w2 = fh.readline().rstrip().split(',')
    return w1, w2

def get_wire_path(w, start_loc=np.array([0, 0])):
    # Reads list of wire paths and returns a list of tuple
    # coordinates that the wire passes through
    
    direction_dict = {'U':np.array([-1, 0]), 'D':np.array([1, 0]),
                      'L':np.array([0, -1]), 'R':np.array([0, 1])}
    wire_locs = []
    wire_locs.append(start_loc)
    current_loc = start_loc
    for move in w:
        d = move[0]
        direction = direction_dict[d]
        
        dist = int(move[1:])
        
        for _ in range(dist):
            current_loc = current_loc+direction
            wire_locs.append(current_loc)
    return [tuple(wl) for wl in wire_locs]

def get_wire_path_timing(w, start_loc=np.array([0, 0])):
    # Reads list of wire paths and returns:
    # (1) a list of tuple coordinates that the wire passes through
    # (2) a dictionary of steps required to reach each coordinate
    
    direction_dict = {'U':np.array([-1, 0]), 'D':np.array([1, 0]),
                      'L':np.array([0, -1]), 'R':np.array([0, 1])}
    wire_locs = []
    loc_times = {}
    
    wire_locs.append(start_loc)
    current_loc = start_loc
    current_time = 0
    for move in w:
        d = move[0]
        direction = direction_dict[d]
        dist = int(move[1:])
        for _ in range(dist):
            current_loc = current_loc+direction
            wire_locs.append(current_loc)
            
            current_time = current_time+1
            if tuple(current_loc) not in loc_times:
                loc_times[tuple(current_loc)] = current_time
            elif current_time < loc_times[tuple(current_loc)]:
                loc_times[tuple(current_loc)] = current_time

            
    return [tuple(wl) for wl in wire_locs], loc_times
        
def shared_paths(path1, path2):
    sp = (set(path1)&set(path2))
    sp.remove((0,0))
    return sp

def calc_dist(loc):
    return np.abs(loc[0])+np.abs(loc[1])
    
    

fn = '03.txt'
w1, w2 = file_to_wire_directions(fn)
path1, t1 = get_wire_path_timing(w1)
path2, t2 = get_wire_path_timing(w2)
shared = shared_paths(path1, path2)

# Part A
distances = []
for s in shared:
    distances.append(calc_dist(s))
print(min(distances))

# Part B
times = []
for s in shared:
    times.append(t1[s]+t2[s])
print(min(times))
