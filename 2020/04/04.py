def input_passports(fn):
    passports = []  # list of dicts
    with open(fn) as fh:
        passport = {}
        for line in fh.readlines():
            if line == '\n':
                passports.append(passport)
                passport = {}
            else:
                pairs = line.rstrip().split(' ')
                for pair in pairs:
                    [key, val] = pair.split(':')
                    passport[key] = val
    passports.append(passport)
    return passports


def check_valid(p):
    if len(p.keys()) == 8:
        return True
    if len(p.keys()) == 7:
        if 'cid' not in p.keys():
            return True
    return False


def check_byr(p):
    if 'byr' not in p:
        return False
    byr = p['byr']
    if len(byr) == 4:
        if 1920 <= int(byr) <= 2002:
            return True
    return False


def check_iyr(p):
    if 'iyr' not in p:
        return False
    iyr = p['iyr']
    if len(iyr) == 4:
        if 2010 <= int(iyr) <= 2020:
            return True
    return False


def check_eyr(p):
    if 'eyr' not in p:
        return False
    eyr = p['eyr']
    if len(eyr) == 4:
        if 2020 <= int(eyr) <= 2030:
            return True
    return False


def check_hgt(p):
    if 'hgt' not in p:
        return False
    hgt = p['hgt']
    if 'cm' in hgt:
        if 150 <= int(hgt[:-2]) <= 193:
            return True
    elif 'in' in hgt:
        if 59 <= int(hgt[:-2]) <= 76:
            return True
    return False


def check_hcl(p):
    if 'hcl' not in p:
        return False
    hcl = p['hcl']
    if hcl[0] == '#':
        if all([x in '0123456789abcdef' for x in hcl[1:]]):
            return True
    return False


def check_ecl(p):
    if 'ecl' not in p:
        return False
    ecl = p['ecl']
    if ecl in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']:
        return True
    return False


def check_pid(p):
    if 'pid' not in p:
        return False
    pid = p['pid']
    if len(pid) == 9:
        if all([x in '0123456789' for x in pid]):
            return True
    return False


passports = input_passports('04.txt')

# Part 1
n_valid = 0
for p in passports:
    if check_valid(p):
        n_valid += 1
print(f"Part 1:\t{n_valid}")

# Part 2
n_valid = 0
for p in passports:
    if all([check_byr(p), check_iyr(p), check_eyr(p), check_hgt(p),
           check_hcl(p), check_ecl(p), check_pid(p)]):
        n_valid += 1
print(f"Part 2:\t{n_valid}")
