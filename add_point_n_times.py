import sage
import math
from functools import lru_cache

def add_point_4(r, s, t, u, delta, R):
  r, s, t, u, delta = R(r), R(s), R(t), R(u), R(delta) # R(2) inverse and multiply 
  two = R(2)
  try:
    two_inverse = ~two
    if two * two_inverse != R(1):
        return None
    
    # Calculate the point coordinates
    x = (r*t + s*u*delta) * two_inverse
    y = (r*u + s*t) * two_inverse
    
    return (x, y)
            
  except (ZeroDivisionError, TypeError):
      return None
    
def add_point(r, s, t, u, d, R):
  r, s, t, u, d = R(r), R(s), R(t), R(u), R(d) # R(2) inverse and multiply 
    
  # Calculate the point coordinates
  x = (r*t + s*u*d)
  y = (r*u + s*t)
    
  return (x, y)
            

def self_add_optimized(n,r,s, delta, R):
  first_two_power = math.floor(math.log2(n))
  res = self_add_two_power_new(first_two_power, r, s, delta, R)
  n -= 2**first_two_power
  while (n > 0):
    next_two_power = math.floor(math.log2(n))
    next_val = self_add_two_power_new(next_two_power, r, s, delta, R)
    new_res = add_point(res[0], res[1], next_val[0], next_val[1], delta, R)
    res = new_res
    n -= 2 ** next_two_power
  # print(res)
  return res

@lru_cache
def self_add_two_power_new(two_power, r, s, delta, R):
  if two_power == 0:
    return (r,s)
  
  prev_r, prev_s = self_add_two_power_new(two_power - 1, r, s, delta, R)
  return add_point(prev_r, prev_s, prev_r, prev_s, delta, R)

def self_add_bruteforce(n, r, s, delta, R):
  ans = (r, s)
  for _ in range(n-1):
    ans = add_point(ans[0],ans[1],r,s,delta,R)
  return ans

self_add_two_power_new.cache_clear()
# print(self_add(5,2,0,-3,IntegerRing()) == self_add_bruteforce(5,2,0,-3,IntegerRing())) # (2,0)
# print(self_add(100,0,14,12,IntegerModRing(31)) == self_add_bruteforce(100,0,14,12,IntegerModRing(31))) # (2,0)
# print(self_add_optimized(6,7,43,2,IntegerModRing(150)))
# print(math.gcd(0, 50), math.gcd(20, 50))
# print(self_add_optimized(18,3,2,2,IntegerModRing(150)))
# print(math.gcd(0, 50), math.gcd(30, 50))
# Test
# test_ans = (1,1)
  
# print(test_ans)
