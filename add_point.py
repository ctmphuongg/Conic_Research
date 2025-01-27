import sage

def add_point(r, s, t, u, delta, R):
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
  
  
  # return ((r*t + s*u*delta)/two, (r*u + s*t)/two)

# print(add_point(4,2,-4,-2,3,IntegerModRing(7))) # (0, 6)
# print(add_point(2,0,-2,0,3,IntegerModRing(15))) # (3, 0)
# print(add_point(1,1,1,1,-3,IntegerRing())) # (3, 0)

def gen_table(n):
  R = IntegerModRing(n)
  table = [[0] * (n**2) for _ in range(n**2)]
  
  
  for i in range(n):
    for j in range(n):
      for x in range(n):
        for y in range(n):
          ans = add_point(i, j, x, y, -3, R)
          table[i*n+j][x*n+y] = add_point(i, j, x, y, -3, R)
          
  for i in range(n**2):
    print(table[i])
  return table

# gen_table(15)


  
