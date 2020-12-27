import re
from operator import attrgetter


class Group:
    def __init__(self, line, team, num):
        self.units = int(re.search(r'(\d*) units', line).group(1))
        self.hp = int(re.search(r'(\d*) hit points', line).group(1))

        weakto = []
        if 'weak' in line:
            weakto = re.search(r'weak to ([\s\w\,]*)', line).group(1)
            weakto = weakto.split(', ')
        self.weakto = weakto

        immuneto = []
        if 'immune' in line:
            immuneto = re.search(r'immune to ([\s\w\,]*)', line).group(1)
            immuneto = immuneto.split(', ')
        self.immuneto = immuneto

        dmg, dmgtype = re.findall(r'(\d*) (\w*) damage', line)[0]
        dmg = int(dmg)
        self.dmg = dmg
        self.dmgtype = dmgtype

        self.initiative = int(re.search(r'initiative (\d*)', line).group(1))

        self.team = team

        self.num = num

        self.calc_effpower()
        self.calc_element_mods()

    def __repr__(self):
        return '_'.join([self.team, str(self.num)])

    def calc_effpower(self):
        self.effpower = self.units * self.dmg

    def calc_element_mods(self):
        elems = ['bludgeoning', 'radiation', 'slashing', 'cold', 'fire']
        elem_mods = {el: 1 for el in elems}
        for el in elems:
            if el in self.weakto:
                elem_mods[el] = 2
            elif el in self.immuneto:
                elem_mods[el] = 0
        self.elem_mods = elem_mods


def load_groups(fn, boost=0):
    groups = {}
    for teams in open(fn).read().split('\n\n'):
        lines = teams.split('\n')
        for num, line in enumerate(lines):
            if 'Immune System' in line:
                team = 'imnsys'
                groups[team] = []
            elif 'Infection' in line:
                team = 'infect'
                groups[team] = []
            else:
                groups[team].append(Group(line, team, num))
    for g in groups['imnsys']:
        g.dmg += boost
        g.calc_effpower()
    return groups


def choose_targets(groups):
    attgrps = []
    [attgrps.extend(g) for g in groups.values()]

    # sort groups by initative and then by effective power
    attgrps.sort(key=attrgetter('initiative'), reverse=True)
    attgrps.sort(key=attrgetter('effpower'), reverse=True)
    defgrps = [g for g in attgrps]
    # [print(g, g.effpower, g.initiative) for g in attgrps]

    targets = {}
    for attgrp in attgrps:
        # Choose target
        defgrps.sort(key=attrgetter('initiative'), reverse=True)
        defgrps.sort(key=attrgetter('effpower'), reverse=True)

        # Calc attack modifier for attacker dmgtype
        def_mods = {d: d.elem_mods[attgrp.dmgtype] for d in defgrps}
        defgrps.sort(key=lambda d: def_mods[d], reverse=True)

        for defgrp in defgrps:
            if defgrp.team == attgrp.team:
                continue
            elif defgrp in targets.values():
                continue
            elif defgrp.elem_mods[attgrp.dmgtype] == 0:
                continue
            else:
                targets[attgrp] = defgrp
                # print(f"Target:\t{defgrp}\n")
                # defgrps.remove(defgrp)
                break

    return targets


def attack(groups, targets):
    attgrps = [a for a in targets.keys()]
    attgrps.sort(key=attrgetter('initiative'), reverse=True)
    for attgrp in attgrps:
        defgrp = targets[attgrp]
        if attgrp.units < 1:
            continue
        if defgrp.units < 1:
            continue

        dmg = attgrp.effpower * defgrp.elem_mods[attgrp.dmgtype]
        units_killed = int(dmg / defgrp.hp)
        if units_killed > defgrp.units:
            units_killed = defgrp.units
        defgrp.units -= units_killed

        defgrp.calc_effpower()
        if defgrp.units < 1:
            defgrp.units = 0
            groups[defgrp.team].remove(defgrp)
    return groups


def combat(groups):
    prev_rg = remaining_units(groups)
    while all([len(g) > 0 for g in groups.values()]):
        targets = choose_targets(groups)
        groups = attack(groups, targets)
        rg = remaining_units(groups)
        if rg == prev_rg:
            break
            print('STALEMATE')
            return False
        prev_rg = rg
    return groups


def remaining_units(groups):
    ans = 0
    for team, group in groups.items():
        for g in group:
            ans += g.units
    return ans


# Part 1
groups = load_groups('24.txt')
groups = combat(groups)
print(f"Part 1:\t{remaining_units(groups)}")

# Part 2
boost = 1
while True:
    groups = load_groups('24.txt', boost=boost)
    groups = combat(groups)
    if groups:
        for team, gs in groups.items():
            if len(gs) > 0:
                winner = team
        if winner == 'imnsys':
            print(f"Part 2:\t{remaining_units(groups)}")
            break
    boost += 1
