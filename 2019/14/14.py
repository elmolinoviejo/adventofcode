
# Load data
# reduce each product to constituent reactants add to new list
# reduce list to sum amount of each product
# check if all are ore products
# repeat

class Reactions():
	def __init__(self, rxns):
		self.rxns = rxns

		self.ore_products = []
		self.product_inds = {}
		for ind, rx in enumerate(rxns):
			if 'ORE' in rx[0].keys():
				self.ore_products.extend(list(rx[1].keys()))
			self.product_inds[list(rx[1].keys())[0]] = ind

def products_to_reactants(r, all_products):
	all_reactants = []
	for p, np in all_products:
		if p in r.ore_products:
			all_reactants.append((p, np))
		else:
			

def parse_reactions(fn):
	with open(fn, 'r') as fh:
		rxns = []
		for ind, l in enumerate(fh):
			rx = tuple([dict(), dict()])
			l = l.rstrip().split(' => ')
			# Product
			np, p = l[1].split(' ')
			rx[1][p] = int(np)
			# Reactants
			for rlist in l[0].split(', '):
				nr, r = rlist.split(' ')
				rx[0][r] = int(nr)
			rxns.append(rx)
	return rxns


rxns = parse_reactions('14_test1.txt')
r = Reactions(rxns)
print(r.ore_products)

all_products = [('FUEL', 1)]


print(r.product_inds)