import re


def load_rules_messages(fn):
    messages = open(fn).read().split('\n\n')[1].split('\n')

    raw_rules = open(fn).read().split('\n\n')[0].split('\n')
    rules = {}
    for line in raw_rules:
        [rnum, rule] = line.split(': ')
        rnum = int(rnum)
        if '"' in rule:
            rule = str(rule[1:-1])
            rules[rnum] = [rule]
        else:
            rule = rule.split(' ')
            int_rule = [int(x) if x != '|' else x for x in rule]
            rules[rnum] = int_rule

    return rules, messages


def replace_rules(rule, rules):
    new_rule = []
    for ind, r in enumerate(rule):
        if isinstance(r, str):
            new_rule.append(r)
        else:
            if '|' in rules[r]:
                new_rule.extend(['('] + rules[r] + [')'])
            else:
                new_rule.extend(rules[r])
    return new_rule


def get_rule(rnum, rules):
    final_rule = rules[rnum]
    while any([isinstance(x, int) for x in final_rule]):
        final_rule = replace_rules(final_rule, rules)
    exp = ''.join(['^'] + final_rule + ['$'])
    return exp


rules, messages = load_rules_messages('19.txt')

# Part 1
exp = get_rule(0, rules)

ans = 0
for m in messages:
    if re.search(exp, m):
        ans += 1
print(f"Part 1:\t{ans}")

# Part 2
# get each rule
r42 = get_rule(42, rules)[1:-1]
r31 = get_rule(31, rules)[1:-1]

exp_insert = ''
for _ in range(5):
    exp_insert = ''.join(['(''|((', r42, ')', exp_insert, '(', r31, ')))'])
exp_insert = ''.join(['((', r42, ')', exp_insert, '(', r31, '))'])

exp = ''.join([r42, ')+(', exp_insert])
exp = '^(' + exp + ')$'

ans = 0
for m in messages:
    if re.search(exp, m):
        ans += 1
print(f"Part 2:\t{ans}")
