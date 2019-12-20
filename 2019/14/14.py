import numpy as np


class Reactions():
    def __init__(self, rxns):
        self.rxns = rxns
        self.product_inds = dict()
        self.all_reactants = dict()
        self.all_products = dict()

        for r_ind, (reacs, prods)in enumerate(self.rxns):
            for prod in prods.keys():
                self.product_inds[prod] = r_ind

    def get_all_rps(self):
        self.all_reactants = {p: [] for p in self.product_inds.keys()}
        while not all(['ORE' in r for r in self.all_reactants.values()]):
            for rind, product in enumerate(self.product_inds):
                if product not in self.all_reactants:
                    self.all_reactants[product] = []
                for reactant in self.all_reactants[product]:
                    if reactant == 'ORE':
                        continue
                    self.all_reactants[product].extend(self.all_reactants[reactant])
                reactants = self.rxns[rind][0]
                self.all_reactants[product].extend([r for r in reactants.keys()])

        for p, reactants in self.all_reactants.items():
            self.all_reactants[p] = set(reactants)

        for p, reactants in self.all_reactants.items():
            for r in reactants:
                if r not in self.all_products:
                    self.all_products[r] = set()
                self.all_products[r].add(p)
        self.all_products['FUEL'] = set()


def products_to_reactants(r, all_products):
    all_reactants = []
    for prod, num_prod in all_products:
        if r.all_products[prod] & set([p for p, _ in all_products]):
            all_reactants.append((prod, num_prod))
        else:
            rxn_ind = r.product_inds[prod]
            num_prod_from_rxn = r.rxns[rxn_ind][1][prod]
            if num_prod > num_prod_from_rxn:
                multiplier = int(np.ceil(num_prod/num_prod_from_rxn))
            else:
                multiplier = 1

            for reac, num_reac in r.rxns[rxn_ind][0].items():
                all_reactants.append((reac, int(num_reac)*multiplier))
    return all_reactants


def consolidate_products(all_products):
    product_counts = {}
    for p, nump in all_products:
        if p not in product_counts:
            product_counts[p] = nump
        else:
            product_counts[p] += nump
    product_counts = [(p, nump) for p, nump in product_counts.items()]
    return product_counts


def parse_reactions(fn):
    with open(fn, 'r') as fh:
        rxns = []
        for ind, l in enumerate(fh):
            rx = tuple([dict(), dict()])
            l = l.rstrip().split(' => ')
            # Product
            nump, p = l[1].split(' ')
            rx[1][p] = int(nump)
            # Reactants
            for rlist in l[0].split(', '):
                numr, reactant = rlist.split(' ')
                rx[0][reactant] = int(numr)
            rxns.append(rx)
    return rxns


reactions = Reactions(parse_reactions('14_test3.txt'))
reactions.get_all_rps()

# rxn_steps = []
all_products = [('FUEL', 1)]
print(all_products)
end_cond = False
while not end_cond:
# for _ in range(6):
    all_products = products_to_reactants(reactions, all_products)
    all_products = consolidate_products(all_products)
    print(all_products)
    if len(all_products) == 1 and all_products[0][0] == 'ORE':
        end_cond = True

answer_a = all_products[0][1]
print(answer_a)

# For Part B, run all reactions in reverse and start with 1E12 ORE