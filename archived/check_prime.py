def check_prime(n):
  for a in range(n):
    condition_1 = False
    condition_2 = True
    
    if a**(n-1) % n == 1:
      condition_1 = True
    
    for r in range(2, n):
      
      if check_prime(r) and (n-1) % r == 0 and a**((n-1)//r) % n == 1:
        condition_2 = False
        
    if condition_1 and condition_2:
      return True
  return False

# print(check_prime(5))
# print(check_prime(7))
# print(check_prime(12))