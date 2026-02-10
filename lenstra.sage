from sage.all import EllipticCurve, IntegerModRing, gcd, primes, randint, log, floor
import re

def lenstra_method(N, B):
    R = IntegerModRing(N)

    x0 = randint(1, N - 1)
    y0 = randint(1, N - 1)
    a  = randint(1, N - 1)

    b = R(y0)^2 - R(x0)^3 - R(a)*R(x0)

    disc = 4*(a^3) + 27*(b^2)
    g = gcd(disc, N)
    if 1 < g < N:
        return g
    if g == N:
        return "failure"

    E = EllipticCurve(R, [a, b])
    P = E(x0, y0)

    # print(f"(x,y) = ({P[0]}, {P[1]})")

    for p in primes(2, B + 1):
        e = 1
        while p^e < N:
            e += 1
        k = p^e

        try:
            P = k * P
            # print(f"(x,y) = ({P[0]}, {P[1]})")

        except ZeroDivisionError as err:
            # Inversion failed → extract factor
            # Sage raises ZeroDivisionError when inverse mod N doesn't exist
            # The offending denominator is usually in err.args
            m = re.search(r'Inverse of (\d+) does not exist', str(err))
            if m:
                v = int(m.group(1))
                g = gcd(v, N)
                if 1 < g < N:
                    return g
            return "failure"

    return "failure"


if __name__ == "__main__":
    N = 583421287793
    B = 12762
    factor = lenstra_method(N, B)
    print("Factor found:", factor)
