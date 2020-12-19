import re


def get_exp_list(fn):
    exp_list = [g for g in open(fn).read().split('\n')]
    return exp_list


def get_next_parens(exp):
    pc = 0
    ind1, ind2 = None, None
    for ind, val in enumerate(exp):
        if val == '(':
            if ind1 is None:
                ind1 = ind
            pc += 1
        elif val == ')':
            if pc == 1:
                ind2 = ind
            pc -= 1
        if (ind1 is not None) and (ind2 is not None):
            return exp[:ind1], exp[ind1 + 1:ind2], exp[ind2 + 1:]


def aoc_eval(exp):
    # Base case - final value
    if all([x not in exp for x in ['+', '*', '(']]):
        return int(exp)
    # With no parentheses
    elif '(' not in exp:
        sub_exp_match = re.search(r'(\d+ [\+\*] \d+)(.*)$', exp)
        sub_exp, rhs = sub_exp_match[1], sub_exp_match[2]
        return aoc_eval(str(eval(sub_exp)) + rhs)
    # Satisfy parentheses first
    elif '(' in exp:
        lhs, sub_exp, rhs = get_next_parens(exp)
        return aoc_eval(lhs + str(aoc_eval(sub_exp)) + rhs)


def get_next_plus(string):
    m1, m2 = re.search(
        r'(\d+|(\([\d\*\s]*\))) \+ (\d+|(\([\d\*\s]*\)))',
        string).span(0)
    return string[:m1], string[m1:m2], string[m2:]


def aoc_eval2(exp):
    # Base case - final value
    if all([x not in exp for x in ['+', '*', '(']]):
        return int(exp)
    # With no parentheses
    elif '(' not in exp:
        # Satisfy addition first
        if ('+' in exp) and ('*' in exp):
            lhs, sub_exp, rhs = get_next_plus(exp)
            new_list = ''.join([str(lhs), str(aoc_eval2(sub_exp)), str(rhs)])
            return aoc_eval2(new_list)
        else:
            sub_exp_match = re.search(r'(\d+ [\+\*] \d+)(.*)$', exp)
            sub_exp, rhs = sub_exp_match[1], sub_exp_match[2]
        return aoc_eval2(str(eval(sub_exp)) + rhs)
    # Satisfy parentheses first
    elif '(' in exp:
        lhs, sub_exp, rhs = get_next_parens(exp)
        return aoc_eval2(lhs + str(aoc_eval2(sub_exp)) + rhs)


# Part 1
ans = sum([aoc_eval(exp) for exp in get_exp_list('18.txt')])
print(f"Part 1:\t{ans}")

# Part 2
ans = sum([aoc_eval2(exp) for exp in get_exp_list('18.txt')])
print(f"Part 2:\t{ans}")
