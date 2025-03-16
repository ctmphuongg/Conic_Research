from add_point_n_times import self_add_optimized, add_point
import math
from sage.all import IntegerModRing, gcd
import random

'''
# Test generate values 
def run_example(N, trials=1):
    """Run the algorithm for a given N and display results"""
    print(f"Running with N = {N}")
    
    for i in range(trials):
        result = generate_values(N)
        if result:
            x, y, delta = result
            print(f"Trial {i+1}:")
            print(f"  x = {x}")
            print(f"  y = {y}")
            print(f"  delta = {delta}")
            print(f"  delta mod 4 = {delta % 4}")
            print(f"  Verification: x² - delta·y² = {(x**2 - delta * y**2) % N}, should equal 1")
            print()
        else:
            print(f"Trial {i+1}: No solution found")
            print()

# Run examples with different moduli
print("Testing with different moduli:")
run_example(N=17, trials=3)
run_example(N=24, trials=3)
run_example(N=101, trials=3)
'''

def find_factor(N, x, y, delta):
    # print(x, y, delta)
    mult = 1
    R = IntegerModRing(N)
    B = math.floor(N**(mult/6))
    M = 1
    for p in range(2, B+1):
        if is_prime(p):
            power = math.floor(math.log(B, p))
            M *= power

    x1, y1 = self_add_optimized(M, x, y, delta, R)
    # print(x1, y1)
    Z = IntegerRing()
    x1 = Z(x1)
    y1 = Z(y1)
    first_div = gcd(x1-1, N)
    if 1 < first_div < N:
        return first_div
    sec_div = gcd(y1, N)
    if 1 < sec_div < N:
        return sec_div
        # mult += 1

    return N 

def factorization(N, method="fact"):
    """
    Factorize N using elliptic curve method
    
    Args:
        N: Number to factorize
        method: "fact" or "p-1" factorization method
    
    Returns:
        Tuple of (factor, attempts) where factor is a non-trivial factor of N (or N if not found)
        and attempts is the number of generation attempts made
    """
    delta = 2
    max_attempts = 5
    
    for attempt in range(1, max_attempts):
        i = random.randint(1, 5)
        x = int(((3 + 2*math.sqrt(2))**i + (3 + 2*math.sqrt(2))**i) / 2) % N
        y = int(((3 + 2*math.sqrt(2))**i + (3 + 2*math.sqrt(2))**i) / (2*math.sqrt(2))) % N
        
        if method == "p-1":
            factor = find_factor(N, x, y, delta)
            if 1 < factor < N:
                return factor, attempt
        else:
            M = random.randint(1, N)
            P = (x, y)
            R = IntegerModRing(N)
            
            for B in range(1, M):
                g = gcd(P[0]-1, N)
                if 1 < g < N:  # Fixed condition to check for non-trivial factor
                    return g, attempt
                P = self_add_optimized(B, P[0], P[1], delta, R)
    
    return N, max_attempts

def format_result(N, result):
    """Format factorization result consistently"""
    factor, attempts = result
    if factor == N:
        return f"No non-trivial factor found for {N} after {attempts} attempts"
    else:
        return f"Found factor {factor} of {N} after {attempts} {'attempt' if attempts == 1 else 'attempts'}"
  

print("Factor of 20", factorization(20, "p-1"))
print("Factor of 120", factorization(120, "fact"))
print("Factor of 55", factorization(55, "p-1"))
print("Factor of 87", factorization(87, "fact"))
print("Factor of 10509", factorization(10509, "p-1"))
print("Factor of 249000", factorization(249000, "fact"))

  
  