import re


def read_rules(fn):
    field_rules = {}
    lines = [g for g in open(fn).read().split('\n')]
    for line in lines:
        field = re.search(r'([\w\s]*)\:', line).group(1)
        ranges = re.findall(r'(\S+) or (\S+)', line)[0]
        num_list = []
        for r in ranges:
            n1, n2 = r.split('-')
            num_list.extend([x for x in range(int(n1), int(n2) + 1)])
        field_rules[field] = set(num_list)

    return field_rules


def read_ticket(fn):
    ticket = open(fn).read().rstrip().split(',')
    ticket = [int(x) for x in ticket]
    return ticket


def read_other_tickets(fn):
    other_tickets = []
    lines = [g for g in open(fn).read().split('\n')]
    for line in lines:
        ot = line.split(',')
        ot = [int(x) for x in ot]
        other_tickets.append(ot)
    return other_tickets


def invalid_tickets(other_tickets, field_rules):
    valid_tickets = []
    val_sum = 0

    all_frs = set.union(*field_rules.values())
    for ticket in other_tickets:
        val_sum += sum([n for n in ticket if n not in all_frs])
        if all([n in all_frs for n in ticket]):
            valid_tickets.append(ticket)

    return val_sum, valid_tickets


def match_fields_inds(tickets, field_rules):
    field_inds = {f: set(range(20)) for f in field_rules.keys()}
    ind_vals = {i: set() for i in range(20)}
    for ticket in tickets:
        [ind_vals[ind].add(val) for ind, val in enumerate(ticket)]

    # Determine possibile inds for each rule
    for field, rule in field_rules.items():
        for ind, vals in ind_vals.items():
            if not vals.issubset(rule):
                field_inds[field].remove(ind)

    # Iterate to identify only possible inds for each field
    final_inds = {}
    while(len(final_inds)) < len(field_rules):
        matched_inds = [x for x in final_inds.values()]
        for field, fi in field_inds.items():
            if len(fi) == 1:
                final_inds[field] = list(fi)[0]
            for mi in matched_inds:
                if mi in field_inds[field]:
                    field_inds[field].remove(mi)

    return final_inds


field_rules = read_rules('16_rules.txt')
ticket = read_ticket('16_ticket.txt')
other_tickets = read_other_tickets('16_other_tickets.txt')

val_sum, valid_tickets = invalid_tickets(other_tickets, field_rules)
print(f"Part 1:\t{val_sum}")

# Part 2
final_inds = match_fields_inds([ticket] + valid_tickets, field_rules)
val_product = 1
for field, fi in final_inds.items():
    if 'departure' in field:
        val_product *= ticket[fi]
print(f"Part 2:\t{val_product}")
