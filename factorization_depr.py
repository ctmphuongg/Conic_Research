from add_point_n_times import self_add_optimized, add_point
import math
import sage
from collections import defaultdict

# curve1 = C(N)  # C(Z/NZ)
# curve2 = C(p)  # C(Z/pZ) 
  
# x^2 - dy^2 = 1
def find_new_prime(orgN, p, q, curve_N, point, delta):
  if orgN % p != 0:
    return {}
  q_points = set([(1,0)])
  multiplier = 1
  point_q_mult = self_add_optimized(q, point[0], point[1], delta, curve_N )  # k = multiple of q
  
  while point_q_mult not in q_points:
    N = orgN
    factors = {}
    print(point_q_mult)
    
    while (N != 1):
      first_divisor = math.gcd(N, point_q_mult[0] - 1) # find gcd(N, x' - 1)
      second_divisor = math.gcd(N, point_q_mult[1]) # find gcd(N, y')
      if first_divisor != N and second_divisor != N:
        largest_divisor = max(first_divisor, second_divisor)
      elif first_divisor != N:
        largest_divisor = first_divisor
      elif second_divisor != N:
        largest_divisor = second_divisor
      else:
        # print("Out loop", N, first_divisor, second_divisor)
        break
      
      new_factor = N // largest_divisor # Guarantee divides
      factors[new_factor] = factors.get(new_factor, 0) + 1
      # print(N, first_divisor, second_divisor, largest_divisor)
      N = largest_divisor
  
    if N % p == 0:
      factors[p] = factors.get(p, 0) + 1
      new_factor = N // p
      factors[new_factor] = factors.get(new_factor, 0) + 1
    elif N != 1:
      factors[N] = factors.get(N, 0) + 1
    print(factors)
    q_points.add(point_q_mult)
    multiplier += 1
    point_q_mult = self_add_optimized(q*multiplier, point[0], point[1], delta, curve_N )  # k = multiple of q
    
  return factors

def legendre_symbol(a, p):
    """Compute the Legendre symbol (a/p) using Euler's criterion."""
    if p <= 1 or p % 2 == 0:
        return -1
    
    a = a % p
    if a == 0:
        return 0
    return pow(a, (p - 1) // 2, p) if pow(a, (p - 1) // 2, p) in (0, 1) else -1


# def factor(N, point, delta):
#     multiplier = 2
#     P = point
#     R = IntegerModRing(N)
    
#     q_max = math.ceil(math.sqrt(N))
#     while multiplier <= q_max:
#         try:
#             P = add_point(P[0], P[1], point[0], point[1], delta, R)
#         except ZeroDivisionError:
#             return -2
            
#         # Convert ring elements to integers before modulo operation
#         x_int = int(P[0].lift())  # Convert from ring element to integer
#         y_int = int(P[1].lift())  # Convert from ring element to integer
        
#         print(multiplier, x_int, y_int)
#         # Case: q = p-1
#         q = multiplier
#         p = q + 1
#         if is_prime(p) and legendre_symbol(delta, p) == 1:
#             print("Pass case 1")
#             if (x_int % p == 1) and (y_int % p == 0):
#                 f_div = math.gcd(x_int-1, N)
#                 if f_div != 1 and f_div != N:
#                   return f_div
#                 s_div = math.gcd(y_int, N)
#                 if s_div != 1 and s_div != N:
#                   return s_div
        
#         # Case q = p+1
#         p = q - 1
#         if p > 1 and is_prime(p) and legendre_symbol(delta, p) == -1:
#             print("Pass case 2")
#             if (x_int % p == 1) and (y_int % p == 0):
#                 f_div = math.gcd(x_int-1, N)
#                 if f_div != 1 and f_div != N:
#                   return f_div
#                 s_div = math.gcd(y_int, N)
#                 if s_div != 1 and s_div != N:
#                   return s_div
           
#         # gc = math.gcd(q, N)   
#         # if gc != 1 and gc != N:
#         #   return gc

#         multiplier += 1
        
#     return -1

# N = 120
# p = 5
# curve_N = IntegerModRing(N)
# delta = 2
# q = 6
# known_points_on_N = (3, 2) 
# known_points_on_N = (7, 43)
# N = 21
# p = 3
# curve_N = IntegerModRing(N)
# delta = 5
# q = 4
# known_points_on_N = (3, 2) 
# known_points_on_N = [7, 43]
# print(find_new_prime(N, p, q, curve_N, known_points_on_N, delta))

N = 87
delta = 5
known_points_on_N = [9, 4]
print(factor(N, known_points_on_N, delta))

'''
Observation: Examples are N = 120, p = 5
- From 1 point, we can generate the new results by self-adding multiples of q times until repeat
so we only needs 1 point
    Eg: Point (7, 43) can generate
    (51, 70)
    {12: 1, 5: 1, 2: 1}
    (41, 60)
    {2: 1, 3: 1, 5: 1, 4: 1}
    (51, 50)
    {12: 1, 5: 1, 2: 1}
    
- Different points can have different set of factors
    Eg: Point (3,2) can generate
    (41, 60)
    {2: 1, 3: 1, 5: 1, 4: 1}

- Choosing different prime will generate different factors
    Eg: N=504, Point (3,2)
    p=3: {7: 1, 3: 2, 8: 1} OR (change q mult) {3: 1, 168: 1}| 
    p=7: {7: 1, 3: 1, 24: 1}
- Factors are not necessarily prime or comprehensive (can be factored more)

Questions: 
- How to combine different results? / Choose best factor results

{}: key = prime, val = prime power
120: p=5: {2: 1, 3: 1, 5: 1, 4: 1} OR (change q mult) {12: 1, 5: 1, 2: 1}
150: p=5: {3: 1, 5: 2, 2: 1}
504: p=3: {7: 1, 3: 2, 8: 1} OR (change q mult) {3: 1, 168: 1}| p=7: {7: 1, 3: 1, 24: 1}
'''
