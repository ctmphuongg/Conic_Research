from sage.all import gcd, inverse_mod, Integers, var, prime_range
from random import randint

from sage.all import Integers, cached_function

def add_point(P1, P2, d, R):
    """
    Add two points P1 = (r,s) and P2 = (t,u) on the Pell conic x^2 - d*y^2 = 1 over R = Z/NZ.
    Returns (x3, y3) modulo R.
    """
    r, s = P1
    t, u = P2
    x3 = r*t + s*u*d
    y3 = r*u + s*t
    return R(x3), R(y3)


# @cached_function
def self_add_two_power(two_power, P, delta, R):
    """
    Compute 2^k * P on the Pell conic using repeated doubling.
    """
    if two_power == 0:
        return P  # 2^0 * P = P
    
    prev = self_add_two_power(two_power - 1, P, delta, R)
    return add_point(prev, prev, delta, R)


def self_add_optimized(n, P, delta, R):
    """
    Compute n*P on the Pell conic using binary decomposition (double-and-add).
    P is a tuple (r,s), delta is d in x^2 - d*y^2 = 1, R is Z/NZ.
    """
    if n == 0:
        return R(1), R(0)  # identity element

    result = (R(1), R(0))
    # Iterate over bits of n (from most significant to least)
    for bit in reversed(bin(n)[2:]):
        # Double the result each time
        result = add_point(result, result, delta, R)
        if bit == '1':
            # Add P if current bit is 1
            result = add_point(result, P, delta, R)
    return result


def pell_method(NN, B):
    """
    Factor NN using a Pell-conic method with bound B.
    Returns a nontrivial factor or 'failure' if none found.
    """

    R = Integers(NN)  # modular ring
    # Step 1: pick random a, b
    while True:
        a = randint(1, NN-1)
        b = randint(1, NN-1)

        # Quick gcd checks
        g = gcd(a, NN)
        if 1 < g < NN:
            return g
        g = gcd(b, NN)
        if 1 < g < NN:
            return g

        # Step 2: compute d = (a^2 - 1)/b^2 mod NN
        try:
            b_inv = inverse_mod(b^2, NN)
        except ZeroDivisionError:
            return "failure"  # b^2 not invertible, try again

        d = ((a^2-1) * b_inv) % NN
        if d % 4 == 2 or d % 4 == 3:
            break
    d = R(d)    
    xN, yN = R(a), R(b)
    # print(f"(x,y) = ({xN},{yN})")


    # Step 3: iterate over small primes <= B
    primes_list = list(prime_range(2, B+1))
    for p in primes_list:
        # Find e such that p^(e-1) < NN <= p^e
        e = floor(log(B, p))
        E = p**e

        # Multiply point by p^e
        xN, yN = self_add_optimized(E, (xN, yN), d, R)
        # Print points for debugging
        # print(f"(x,y) = ({xN},{yN})")

        # Check gcd for factor
        g = gcd([xN-1, yN, NN])
        if g != 1 and g != NN:
            return g

    return "failure"

if __name__ == "__main__":
    NN = 583421287793
    B = 12762
    factor = pell_method(NN, B)
    print("Factor found:", factor)
    # factor2 = pell_method(357, 6)
    # print("Factor found:", factor2)