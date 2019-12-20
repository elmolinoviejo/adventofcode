import numpy as np
import networkx as nx
import matplotlib.pyplot as plt


class Reaction_Network():
    def __init__(self, reactions):
        self.g = nx.DiGraph()
        self.ore_paths = {}
        self.fuel_paths = {}

        for r_ind, (reacs, prods) in enumerate(reactions):
            for prod, n_prod in prods.items():
                for reac, n_reac in reacs.items():
                    self.g.add_edge(reac, prod, stoic=(n_reac, n_prod), r_ind=r_ind)

        for chem in self.g.nodes:
            if chem != 'ORE':
                self.ore_paths[chem] = nx.all_simple_paths(
                    self.g, 'ORE', chem)
            if chem != 'FUEL':
                self.fuel_paths[chem] = nx.all_simple_paths(
                    self.g.reverse(), 'FUEL', chem)


def parse_reactions(fn):
    with open(fn, 'r') as fh:
        reactions = []
        for ind, l in enumerate(fh):
            reaction = tuple([dict(), dict()])
            l = l.rstrip().split(' => ')
            # Product
            n_prod, prod = l[1].split(' ')
            reaction[1][prod] = int(n_prod)
            # Reactants
            for reac_list in l[0].split(', '):
                n_reac, reac = reac_list.split(' ')
                reaction[0][reac] = int(n_reac)
            reactions.append(reaction)
    return reactions


def products_to_reactants(rn, inventory, direction='ORE'):
    next_inventory = dict()
    if direction == 'ORE':
        all_paths = rn.ore_paths
        stoic_inds = [1, 0]
    elif direction == 'FUEL':
        all_paths = rn.fuel_paths
        stoin_inds = [0, 1]

    # Check if chem is upstream of any other chems
    upstream_chems = set()
    for path_chem, paths in all_paths.items():
        if path_chem in inventory:
            for p in paths:
                upstream_chems.update(set(p[:-1]))
    # print(upstream_chems)

    for chem, n_chem in inventory.items():
        if chem in upstream_chems:
            next_inventory[chem] = n_chem
        else:
            for precursor, attr in rn.g.reverse()[chem].items():
                stoic_precursor = attr['stoic'][stoic_inds[1]]
                stoic_chem = attr['stoic'][stoic_inds[0]]
                n_precursor = int(np.ceil(n_chem/stoic_chem)*stoic_precursor)
                if precursor in next_inventory:
                    next_inventory[precursor] += n_precursor
                else:
                    next_inventory[precursor] = n_precursor

    return next_inventory

r = Reaction_Network(parse_reactions('14_test3.txt'))

# Neighbors of FUEL (or any other node)

# Directed paths from ORE to FUEL or FUEL to ORE
# for prod, ops in r.ore_paths.items():
#     print(prod)
#     print([op for op in ops])

# print(r.g.edges(data='stoic'))

inventory = {'FUEL': 1}  # starting inventory
print(inventory)

end_cond = False
while not end_cond:
    inventory = products_to_reactants(r, inventory)
    print(inventory)
    if len(inventory) == 1 and 'ORE' in inventory:
        end_cond = True
print(inventory['ORE'])




# nx.draw(r.g)
# plt.show()
# nx.draw_networkx_labels(r.g)
