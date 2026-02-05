from sage.all import EllipticCurve, GF, Integers, ZZ, randint, gcd, factorial, prime_powers, primes, IntegerModRing
import random
import math

def ecm_factorization(N, method="fact", max_attempts = 100000):
    """
    Elliptic Curve Method (ECM) for factorization
    
    Args:
        N: Number to factorize
        method: "fact" for factorial method or "p-1" for prime powers method
        max_attempts: Maximum number of attempts to find a factor
        B: Bound for prime powers (if None, will generate random bound)
    """
    if N <= 1:
        return N, 0, 0
    if N % 2 == 0:
        return 2, 0, 0
    
    R = IntegerModRing(N)
    total_additions = 0
    
    for attempt in range(1, max_attempts + 1):
        # Use different seed for each attempt
        # random.seed(attempt)
        B = randint(1, math.ceil(N**(1/3)))
            
        x0 = randint(0, N-1)
        y0 = randint(0, N-1)
        a = randint(0, N-1)
        
        b = (R(y0)**2 - R(x0)**3 - R(a) * R(x0)) % N
        
        try:
            E = EllipticCurve(R, [a, b])
            P = E(x0, y0)
            
            if method == "p-1":
                # For p-1 method: multiply by prime powers up to B
                for p in primes(2, B+1):
                    power = math.floor(math.log(B, p))
                    for _ in range(power):
                        try:
                            P = p * P
                            total_additions += 1
                        except Exception as e:
                            error_info = str(e)
                            for part in error_info.split():
                                try:
                                    v = int(part)
                                    d = gcd(v, N)
                                    if 1 < d < N:
                                        return d, attempt, total_additions
                                except ValueError:
                                    continue
            else:
                # For factorial method: multiply by integers from 1 to B
                for j in range(2, B + 1):
                    try:
                        P = j * P
                        total_additions += 1
                    except Exception as e:
                        error_info = str(e)
                        for part in error_info.split():
                            try:
                                v = int(part)
                                d = gcd(v, N)
                                if 1 < d < N:
                                    return d, attempt, total_additions
                            except ValueError:
                                continue
        except Exception:
            # If curve creation or initial point setup fails, try another curve
            continue
    
    # If we've tried all curves and found no factor, return n
    return N, max_attempts, total_additions
        
  
print("Factor of 20167919", ecm_factorization(20167919))
print("Factor of 180181*181081", ecm_factorization(32627355661))
print("Factor of 3326489*3326489", ecm_factorization(11065529067121))