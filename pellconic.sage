from sage.all import gcd, inverse_mod, Integers, var, prime_range
from random import randint

from sage.all import Integers, cached_function

def add_point(P1, P2, d, R):
    """
    Add two points on conic
    """
    r, s = P1
    t, u = P2
    x3 = r*t + s*u*d
    y3 = r*u + s*t
    return R(x3), R(y3)

def self_add_optimized(n, P, delta, R):
    """
    Optimized addition using 2 power  
    """
    if n == 0:
        return R(1), R(0)

    result = (R(1), R(0)) 
    first = True
    for bit in bin(n)[2:]: 
        if not first:
            result = add_point(result, result, delta, R)  # double

        if bit == '1':
            if first: # First bit, result = P
                result = P
            else: # After that, double prev result, add another P if bit = 1
                result = add_point(result, P, delta, R)  # add P
        
        first = False  # after first bit processed
    return result

def pell_method(N, B):
    """
    Factor N using a Pell-conic method with bound B.
    Returns a nontrivial factor or 'failure' if none found.
    """

    R = Integers(N)  # modular ring
    a = randint(1, N-1)
    b = randint(1, N-1)

    # Quick gcd checks, make sure b invertible
    g = gcd(a, N)
    if 1 < g < N:
        return g
    g = gcd(b, N)
    if 1 < g < N:
        return g

    xN, yN = R(a), R(b)
    b_inv = inverse_mod(b^2, N) # b must be invertible due to prev check
    d = ((a^2-1) * b_inv)

    # print(f"(x,y) = ({xN},{yN})")
    for l in primes(2, B+1):
        # Find e such that l^(e-1) < N <= l^e
        e = ceil(log(N, l))
        E = l^e

        xN, yN = self_add_optimized(E, (xN, yN), d, R)
        # print(f"(x,y) = ({xN},{yN})")

        g = gcd([xN-1, yN, N])
        if g != 1 and g != N:
            return g

    return "failure"

if __name__ == "__main__":
    N = 583421287793
    B = 12762
    factor = pell_method(N, B)
    print("Factor found:", factor)
    # factor2 = pell_method(357, 6)
    # print("Factor found:", factor2)