import math
import random
import time
from sage.all import IntegerModRing, Integer, primes, gcd
from functools import lru_cache

def pollard_factor(N, B):
    a = random.randint(1, N-1)
    d = math.gcd(a, N)
    if d != 1:
        return d
    
    b = a
    for l in primes(1, B+1):
        e = math.ceil(math.log(l, N))
        b = b**(l**e) % N
        d = math.gcd(b-1, N)
        if d != 1:
            if d < N:
                return d
            else:
                return -1
            
    return -1

# print(pollard_factor(391, 19))
print(pollard_factor(357, 6))
