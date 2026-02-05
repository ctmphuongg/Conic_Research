from sage.all import EllipticCurve, GF, Integers, ZZ, randint, gcd, factorial, prime_powers, primes, IntegerModRing
import random
import math
import re

def lenstra_method(N, B):
    x0 = randint(0, N-1)
    y0 = randint(0, N-1)
    a = randint(0, N-1)
    R = IntegerModRing(N)
    
    b = R(y0)**2 - R(x0)**3 - R(a)*R(x0)

    disc = 4*(a**3) + 27*(b**2)
    g = gcd(disc, N)
    if 1 < g < N:
        return g 
    if g == N:
        return "failure"
    
    E = EllipticCurve(R, [a, b])
    P = E(x0, y0)
    
    print(f"(x,y) = ({P[0]}, {P[1]})")
    
    for p in primes(2, B+1):
        e = math.floor(math.log(B, p))
        k = p**e
        
        try:
            P = k * P
            print(k)
            print(f"(x,y) = ({P[0]}, {P[1]})")
        except ZeroDivisionError as err:
            # Failed inversion => possible factor
            # gcd of denominator and N
            m = re.search(r'Inverse of (\d+) does not exist', str(err))
            if m:
                v = int(m.group(1))
                g = gcd(v, N)
                if 1 < g < N:
                    return g
            return "failure"
                    
    return "failure"
   
if __name__ == "__main__":           
    N = 299
    B = 10
    factor = lenstra_method(N, B)
    print("Factor found:", factor)