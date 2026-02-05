from archived.add_point_n_times import *
from functools import lru_cache

def verify(delta, n):
  R = IntegerModRing(n)
  if legendre(delta, R) != -1:
    raise ValueError("Unmatched delta")
  
  return is_prime(delta, R, n)

def check_prime(n):
  if n < 2:
    return False
  for i in range(2, isqrt(n) + 1):
    if n % i == 0:
      return False
  return True
  
def legendre(delta, R):
  for i in R:
    if R(i**2) == R(delta):
      return 1
    
  return -1

@lru_cache(maxsize=None)  # Cache all results
def is_prime(delta, R, n):
  
  if n < 5 or n % 2 == 0:
    return False
  
  if legendre(delta, R) != -1:
    return False
  
  # Loop through points on the Pell conic X² - ΔY² = 4
  for x in R:
    for y in R:
      # Check if point satisfies the Pell conic equation
      if (x**2 - delta*y**2 - 4) % n == 0:
        # Check condition i): (n+1)P = N
        point_n_plus_1 = self_add_optimized(n+1, x, y, delta, R)
        if point_n_plus_1 != (2,0):  # N = (2,0)
          continue
        
        # Check condition ii)
        valid_point = True
        
        for r in range(2, n + 2):
          # if R(r).is_unit() or R(n+1) in R.ideal(r):  # r divides n+1
          if (n+1) % r == 0 and check_prime(r):  # if r is prime

            # Check if (n+1)/r * P = N
            point_div_r = self_add_optimized((n+1)//r, x, y, delta, R)
            if point_div_r == (2,0):
              valid_point = False
              break
        
        if valid_point:
          return True
  
  return False

# The cache can be cleared if needed:
is_prime.cache_clear()
  
# Example usage:
n = 29

for d in range(n):
  delta = -1
  if d % 4 == 1:
    delta = d
  elif d % 4 == 2 or d % 4 == 3:
    delta = d
  
  try:
    result = verify(delta, n)
  except ValueError:
    continue
  else:
    # This block runs if no exception is raised
    print(f"Is {n} prime? {result}")
    break