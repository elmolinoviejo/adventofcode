# Move along shortest_path
# Each step, move to adjacent unknown spot
# update passage_locs, wall_locs, and g
# update shortest path, if current loc in new shortest path, continue
# else reinitialize

def explore_shortest_path(c, g, passage_locs, wall_locs, end_loc, start_loc=(0,0)):
    shortest_path = nx.shortest_path(g, start_loc, end_loc)
    current_loc = start_loc
    
    pass