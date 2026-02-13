import random
from sage.all import gcd, primes, ceil, log

def pollard_method(N, B):
    a = random.randint(1, N - 1)
    d = gcd(a, N)
    if d != 1:
        return d

    b = a
    for l in primes(2, B + 1):
        e = ceil(log(N, l))
        E = l^e
        b = power_mod(b, E, N)
        d = gcd(b - 1, N)
        if d != 1:
            if d < N:
                return d
            else:
                return "failure"

    return "failure"

if __name__ == "__main__":
    print(pollard_method(391, 19))
    print(pollard_method(357, 6))
