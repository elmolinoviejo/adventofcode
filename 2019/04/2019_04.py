import numpy as np
import re

def ascending_digits(n):
    nst = str(n)    
    ascend = True
    for ind in range(len(nst)-1):
        if int(nst[ind])>int(nst[ind+1]):
            return False
    return True

def adjacent_digits(n):
    nst = str(n)
    for ind in range(len(nst)-1):
        if nst[ind]==nst[ind+1]:
            return True
    return False
            
def adjacent_digits2(n):
    for d in set(str(n)):
        for match in re.findall(d+'{2,}', str(n)):
            if len(match)==2:
                return True
    return False

# Part A
n_pw = 0

for n in np.arange(356261, 846303+1):
    if ascending_digits(n):
        if adjacent_digits(n):
            n_pw+=1
            
print(n_pw)

# Part B
n_pw = 0

for n in np.arange(356261, 846303+1):
    if ascending_digits(n):
        if adjacent_digits2(n):
            n_pw+=1
            
print(n_pw)