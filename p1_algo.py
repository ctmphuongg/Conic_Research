import math
import random
import time
from sage.all import IntegerModRing, Integer, primes, gcd
RANDMAX = 1000000000

'''
- a^M mod N = 1, so gcd(a^M - 1, N) = gcd((a^M mod N), N)
- Calculate a^M by ((a^b)^c)^... st b*c*... = M
- mod N so that it's faster
https://en.wikipedia.org/wiki/Algebraic-group_factorisation_algorithm
'''

def mod_pow(base, exponent, modulus):
    """Compute (base^exponent) % modulus efficiently"""
    result = 1
    base = base % modulus
    while exponent > 0:
        if exponent % 2 == 1:
            result = (result * base) % modulus # mult 1 additional base
        exponent = exponent >> 1 # double current
        base = (base * base) % modulus
    return result

def p1_factorize_original(N, max_attempts=10000):
    if N <= 1:
        return N, 0, 0
    if N % 2 == 0:
        return 2, 0, 0
        
    min_B = 1
    max_B = math.ceil(math.sqrt(N))
    attempt = 0
    total_additions = 0
    
    while attempt < max_attempts and min_B < max_B:
        B = random.randint(min_B, max_B)
        
        # Choose a coprime to N
        if N % 2 == 1:
            a = 2
        else: # Actually already cutoff
            a_found = False
            for _ in range(10):
                a = random.randint(2, min(RANDMAX, N-1))
                if math.gcd(a, N) == 1:
                    a_found = True
                    break
            if not a_found:
                return N, attempt, total_additions
        
        # Compute a^M mod N directly
        result = a % N
        for p in primes(2, B+1):
            power = math.floor(math.log(B, p))
            # Calculate (result^(p^power)) mod N
            for _ in range(power):
                result = mod_pow(result, p, N)
                total_additions += 1
        
        # Now result = a^M mod N
        g = math.gcd((result - 1) % N, N)
        
        attempt += 1
        if 1 < g < N:
            return g, attempt, total_additions
        elif g == 1:
            min_B = B+1
        elif g == N:
            max_B = B-1
    
    return N, max_attempts, total_additions
  
def p1_factorize_16(N, B=None, max_attempts=10000):
    """Pollard's p-1 factorization with fixed B = N^(1/6)"""
    if N <= 1:
        return N, 0, 0
        
    if N % 2 == 0:
        return 2, 0, 0
        
    # Set B = N^(1/6) if not provided
    if B is None:
        B = math.floor(N**(1/6))
    
    # Choose a coprime to N
    if N % 2 == 1:
        a = 2
    else:
        for _ in range(10):
            a = random.randint(2, min(10**9, N-1))
            if math.gcd(a, N) == 1:
                break
        else:
            return N, 0, 0  # Failed to find coprime
            
    # Compute a^M mod N directly
    result = a % N
    total_additions = 0
    
    # For each prime p ≤ B
    for p in primes(2, B+1):
        # Calculate power = floor(log_p(B))
        power = math.floor(math.log(B, p))
        
        # Calculate (result^(p^power)) mod N
        p_power = p**power
        result = mod_pow(result, p_power, N)
        total_additions += 1
    
    # Calculate gcd(a^M - 1, N)
    g = math.gcd((result - 1) % N, N)
    
    if 1 < g < N:
        return g, 1, total_additions
    else:
        return N, 1, total_additions  # Indicating failure

# print("Factor of 20:", p1_factorize_original(20))
# print("Factor of 120:", p1_factorize_original(120))
# print("Factor of 55:", p1_factorize_original(55))
# print("Factor of 87:", p1_factorize_original(87))
# print("Factor of 10509:", p1_factorize_original(10509))
# print("Factor of 249000:", p1_factorize_original(249000))

# print("Factor of 20:", p1_factorize_16(20))
# print("Factor of 120:", p1_factorize_16(120))
# print("Factor of 55:", p1_factorize_16(55))
# print("Factor of 87:", p1_factorize_16(87))
# print("Factor of 10509:", p1_factorize_16(10509))
# print("Factor of 249000:", p1_factorize_16(249000))

# success_org = 0
# success_16 = 0

# '''
# N^(1/6) probability:  81.301
# Original probability:  100
# '''
# for x in range(100000):
#     N = random.randint(0, 100000)
#     org_res = p1_factorize_original(N)
#     org_16 = p1_factorize_16(N)
#     success_org += int(org_res != None)
#     success_16 += int(org_16 != None)
#     if x % 1000 == 0:
#         print(str(x) + "/1000000 complete")
  
# print("N^(1/6) probability: ", success_16 / 1000)
# print("Original probability: ", success_org / 1000)
