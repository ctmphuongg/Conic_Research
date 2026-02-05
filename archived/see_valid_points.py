'''
Delta = 3
2 0 1
2 1 2
2 2 4
2 3 8
2 4 32
3 0 1
3 1 6
3 2 18
3 3 54
3 4 162
5 0 1
5 1 6
5 2 30
5 3 150
5 4 750
7 0 1
7 1 8
7 2 56
7 3 392
7 4 2744
11 0 1
11 1 10
11 2 110
11 3 1210
11 4 13310
13 0 1
13 1 12
13 2 156
13 3 2028

Delta = 5
2 0 1
2 1 2
2 2 8
2 3 24
2 4 48
3 0 1
3 1 4
3 2 12
3 3 36
3 4 108
5 0 1
5 1 10
5 2 50
5 3 250
5 4 1250
7 0 1
7 1 8
7 2 56
7 3 392
7 4 2744
11 0 1
11 1 10
11 2 110
11 3 1210
11 4 13310
13 0 1
13 1 14
13 2 182
13 3 2366

Delta = 8
2 0 1
2 1 2
2 2 8
2 3 16
2 4 32
3 0 1
3 1 4
3 2 12
3 3 36
3 4 108
5 0 1
5 1 6
5 2 30
5 3 150
5 4 750
7 0 1
7 1 6
7 2 42
7 3 294
7 4 2058
11 0 1
11 1 12
11 2 132
11 3 1452
11 4 15972
13 0 1
13 1 14
13 2 182
13 3 2366
'''
import sage 

def see_valid_points(delta, R, n):
  counter = 0
  for x in R:
    for y in R:
      if (x**2 - delta*y**2 - 4) % n == 0:
        # print((x, y))
        counter += 1
        
  return counter
        
# msg = "There are {} valid points in this ring".format(see_valid_points(3, IntegerModRing(2**3), 2**3))
# print(msg)

import csv

primes = [2,3,5,7,11,13,17,19]
# primes = [13,17,19]

# Assuming you've already populated arr as in your original code
arr = [[-1] * 5 for _ in range(len(primes))]
for i in range(len(primes)):
    p = primes[i]
    for j in range(5):
      arr[i][j] = see_valid_points(8, IntegerModRing(p**j), p**j)
      print(p, j, arr[i][j])

# Save to CSV
with open('prime_points.csv', 'w', newline='') as csvfile:
    # Create a CSV writer object
    csvwriter = csv.writer(csvfile)
    
    # Write the header row with column names 0-5
    header = ['Prime'] + [str(j) for j in range(5)]
    csvwriter.writerow(header)
    
    # Write the data rows
    for i, row in enumerate(arr):
        # Add the prime number as the first column
        full_row = [primes[i]] + row
        csvwriter.writerow(full_row)

print("CSV file 'prime_points.csv' has been created.")