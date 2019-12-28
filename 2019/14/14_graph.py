import numpy as np
import networkx as nx
# import matplotlib.pyplot as plt


class Reaction_Network():
    def __init__(self, reactions):
        self.g = nx.DiGraph()
        self.ore_paths = {}
        self.fuel_paths = {}

        for r_ind, (reacs, prods) in enumerate(reactions):
            for prod, n_prod in prods.items():
                for reac, n_reac in reacs.items():
                    self.g.add_edge(
                        reac, prod, stoic=(n_reac, n_prod), r_ind=r_ind)

        for chem in self.g.nodes:
            if chem != 'ORE':
                self.ore_paths[chem] = [x for x in nx.all_simple_paths(
                    self.g, 'ORE', chem)]
            if chem != 'FUEL':
                self.fuel_paths[chem] = [x for x in nx.all_simple_paths(
                    self.g.reverse(), 'FUEL', chem)]


def parse_reactions(fn):
    with open(fn, 'r') as fh:
        reactions = []
        for ind, line in enumerate(fh):
            reaction = tuple([dict(), dict()])
            line = line.rstrip().split(' => ')
            # Products
            n_prod, prod = line[1].split(' ')
            reaction[1][prod] = int(n_prod)
            # Reactants
            for reac_list in line[0].split(', '):
                n_reac, reac = reac_list.split(' ')
                reaction[0][reac] = int(n_reac)
            reactions.append(reaction)
    return reactions


def products_to_reactants(rn, inventory, direction='ORE'):
    if direction == 'ORE':
        all_paths = rn.ore_paths
        stoic_inds = [1, 0]
    elif direction == 'FUEL':
        all_paths = rn.fuel_paths
        stoic_inds = [0, 1]
    # Check if chem is upstream of any other chems
    upstream_chems = set([direction])
    for path_chem in inventory.keys():
        if path_chem != direction:
            for path in all_paths[path_chem]:
                upstream_chems.update(path[:-1])
    next_inventory = dict()
    for chem, n_chem in inventory.items():
        if chem in upstream_chems:
            if chem in next_inventory:
                next_inventory[chem] += n_chem
            else:
                next_inventory[chem] = n_chem
        else:
            for precursor, attr in rn.g.reverse()[chem].items():
                stoic_precursor = attr['stoic'][stoic_inds[1]]
                stoic_chem = attr['stoic'][stoic_inds[0]]
                n_precursor = int(np.ceil(
                    n_chem / stoic_chem) * stoic_precursor)
                if precursor in next_inventory:
                    next_inventory[precursor] += n_precursor
                else:
                    next_inventory[precursor] = n_precursor

    return next_inventory


r = Reaction_Network(parse_reactions('14.txt'))
inventory = {'FUEL': 1}  # starting inventory
# print(inventory)

print('Part A')
end_cond = False
while not end_cond:
    inventory = products_to_reactants(r, inventory)
    # print(inventory)
    if len(inventory) == 1 and 'ORE' in inventory:
        end_cond = True
parta_ans = inventory['ORE']
print(parta_ans)

print('Part B')
starting_fuel = [2000000, 5000000]
partb_end_cond = False
n_iter = 1
while not partb_end_cond:
    inventory = {'FUEL': starting_fuel[n_iter]}  # starting inventory

    end_cond = False
    while not end_cond:
        inventory = products_to_reactants(r, inventory)
        if len(inventory) == 1 and 'ORE' in inventory:
            end_cond = True

    n_ore = inventory['ORE']
    if 0 < (n_ore - 1E12) < parta_ans:
        partb_end_cond = True
        print(starting_fuel[n_iter] - 1)
    elif (n_ore - 1E12) > parta_ans:
        starting_fuel.append(
            starting_fuel[n_iter] -
            np.abs(int((starting_fuel[n_iter] -
                        starting_fuel[n_iter - 1]) / 2)))
        n_iter += 1
    elif (n_ore - 1E12) < 0:
        starting_fuel.append(
            starting_fuel[n_iter] +
            np.abs(int((starting_fuel[n_iter] -
                        starting_fuel[n_iter - 1]) / 2)))
        n_iter += 1
