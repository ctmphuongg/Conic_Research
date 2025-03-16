import math

def p1_factorize(N):
  mult = 1
  while mult < 6:
    B = math.floor(N**(mult/6))
    M = 1
    for p in range(2, B+1):
      if is_prime(p):
        power = math.floor(math.log(B, p))
        M *= power