from add_point_n_times import self_add_optimized, add_point
import math
from sage.all import IntegerModRing, primes, Integer, gcd
import random
from functools import lru_cache
import time

@lru_cache(maxsize=None)
def recur_add_x(x, times):
    if times == 1:
        return x
    if times == 0:
        return 1
    
    P = times // 2
    x_P = recur_add_x(x, P)
    x_Q = recur_add_x(x, times - P)
    x_P_Q = recur_add_x(x, (times - P) - P)
    return 2*x_P*x_Q - x_P_Q

def factorization(N, max_attempts=5):
    N = Integer(N)
    total_additions = 0
    
    for attempt in range(1, max_attempts):
        i = random.randint(1, 5)
        I3 = Integer(3)
        I2 = Integer(2) 
        x = int(((I3 + I2*math.sqrt(2))**i + (I3 + I2*math.sqrt(2))**i) / 2) % N
        
        M = random.randint(1, N)
        R = IntegerModRing(N)
        K = R(x)
        
        for B in range(1, M):
            g = math.gcd(K-1, N)
            if 1 < g < N:  
                return g, attempt, total_additions
            recur_add_x.cache_clear()
            K = recur_add_x(K, B)
            total_additions += 1

    return N, max_attempts, total_additions
  
def conic_factorization(N, method="fact", max_attempts=10000):
    if N % 2 == 0:
        return 2, 1, 0
    
    total_additions = 0
    for attempt in range(1, max_attempts+1):
        # Use different seed for each attempt
        # random.seed(attempt)
        
        x = random.randint(1, N-1)
        R = IntegerModRing(N)
        K = R(x)
        
        B = random.randint(1, math.ceil(N**(1/6)))
        print("Attempt ", attempt, " B=", B, " x=", x)
        
        if method == "p-1":
            # For p-1 method: multiply by prime powers up to B
            for p in primes(2, B+1):
                power = math.floor(math.log(B, p)) #power = log_p(B)
                for _ in range(power):
                    recur_add_x.cache_clear()
                    K = recur_add_x(K, p) # K = pK mod N; M = product of p^power
                    total_additions += 1
                    g = math.gcd(K-1, N)
                    if 1 < g < N:
                        return g, attempt, total_additions
        else:
            # For fact method: multiply by integers from 1 to B
            for i in range(1, B+1):
                recur_add_x.cache_clear()
                K = recur_add_x(K, i)
                total_additions += 1
                g = math.gcd(K-1, N)
                if 1 < g < N:
                    return g, attempt, total_additions

    return N, max_attempts, total_additions


# print("Factor of 20", factorization(20))
# print("Factor of 120", factorization(120))
# print("Factor of 55", factorization(55))
'''
Factor of 25117 * 26227 (25117, 1)
Factor of 180181 * 181081 (181081, 1)
'''
# print("Factor of 20167919", conic_factorization(20167919))
# print("Factor of 180181*181081", conic_factorization(32627355661))
# print("Factor of 3326489*3326489", conic_factorization(11065529067121, max_attempts=1000))




# Test both methods with timing
# success_rand = 0
# success_org = 0
# total = 0
# time_rand_total = 0
# time_org_total = 0

# num_tests = 1000000

# for x in range(num_tests):
#     N = random.randint(100, 1000000)
#     if is_prime(N):
#         continue
    
#     recur_add_x.cache_clear()
#     # Test random method with timing
#     start_time = time.time()
#     res_rand, attempts_rand, total_additions_rand = factorization_random(N)
#     end_time = time.time()
#     time_rand = end_time - start_time
#     time_rand_total += time_rand
#     success_rand += int(res_rand != N)
    
#     recur_add_x.cache_clear()
#     # Test original method with timing
#     start_time = time.time()
#     res_org, attempts_org, total_additions_org = factorization(N)
#     end_time = time.time()
#     time_org = end_time - start_time
#     time_org_total += time_org
#     success_org += int(res_org != N)
    
#     total += 1
    
#     if x % 100 == 0:
#         print(f"{x}/{num_tests} complete")
#         print(f"Interim results:")
#         print(f"  Random method: {success_rand}/{total} successes ({success_rand/total*100:.2f}%), avg time: {time_rand_total/total:.6f}s")
#         print(f"  Original method: {success_org}/{total} successes ({success_org/total*100:.2f}%), avg time: {time_org_total/total:.6f}s")
#         print()

# # Print final results
# print("\nFinal Results:")
# print(f"Total non-prime numbers tested: {total}")
# print(f"Random method success rate: {success_rand/total*100:.2f}%")
# print(f"Original method success rate: {success_org/total*100:.2f}%")
# print(f"Random method average time: {time_rand_total/total:.6f} seconds")
# print(f"Original method average time: {time_org_total/total:.6f} seconds")
# print(f"Time difference: {abs(time_rand_total - time_org_total)/total:.6f} seconds per number")

# if time_rand_total < time_org_total:
#     print(f"Random method is {time_org_total/time_rand_total:.2f}x faster")
# else:
#     print(f"Original method is {time_rand_total/time_org_total:.2f}x faster")
    
    
    
# '''
# Random method: 39374/39380 successes (99.98%), avg time: 0.020764s
# Original method: 39370/39380 successes (99.97%), avg time: 0.031232s
# '''