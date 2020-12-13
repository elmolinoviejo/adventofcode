import re
import networkx as nx


def import_to_DiGraph(fn):
    G = nx.DiGraph()
    rules = [g for g in open(fn).read().split('\n')]
    for r in rules:
        re_matches = re.findall(r'((\d+)\s)?(\w+\s\w+)\sbag', r)
        for ind, match in enumerate(re_matches):
            if ind == 0:
                outer_bag = match[2]
            else:
                inner_bag = match[2]
                if inner_bag != 'no other':
                    inner_bag_num = int(match[1])
                    G.add_edge(outer_bag, inner_bag, weight=inner_bag_num)

    return G

G = import_to_DiGraph('07_test.txt')
# G = import_to_DiGraph('07.txt')
print([p for p in G.predecessors('shiny gold')])

# print(len(nx.bfs_predecessors(G, 'shiny gold')))
# print(len([x for x in nx.bfs_predecessors(G, 'shiny gold')]))

# preds = []
# for p, _ in nx.dfs_predecessors(G, 'shiny gold').items():
#     # print(p)
#     preds.append(p)
# print(len(set(preds)))
# print(len(set(preds)))
# print(nx.dfs_successors(G, 'shiny gold'))
# print([x for x in G.adjacency()])
# print(nx.is_branching(G))