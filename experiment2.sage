"""
Experiment to evaluate the number of trials needed for three factorization methods:
- Pell's method
- Pollard's method  
- Williams' method

This script compares how many trials each method needs to successfully factor N = p*q
with an ideal choice of smoothness bound B = e^{sqrt(ln(N) * ln(ln(N)))}
"""

# Import the factorization methods from each file
load("pellconic.sage")
load("pollard.sage")
load("williams.sage")

import random
from collections import defaultdict
from math import log, sqrt, exp

def generate_semiprime(bit_length=20):
    """
    Generate N = p * q
    """
    p = random_prime(2^bit_length, lbound=2^(bit_length-1))
    q = random_prime(2^bit_length, lbound=2^(bit_length-1))
    while p == q:
        q = random_prime(2^bit_length, lbound=2^(bit_length-1))
    N = p * q
    return N, p, q

def compute_ideal_B(N):
    """
    Compute the ideal smoothness bound B = e^{sqrt(ln(N) * ln(ln(N)))}
    """
    ln_N = log(float(N))
    ln_ln_N = log(ln_N)
    B = exp(sqrt(ln_N * ln_ln_N))
    return int(B)

def generate_N_sets(num_tests, bit_length):
    N_values = []
    p_values = []
    q_values = []

    for test_num in range(1, num_tests + 1):
        N, p, q = generate_semiprime(bit_length)
        N_values.append(N)
        p_values.append(p)
        q_values.append(q)

    return N_values, p_values, q_values

# def run_experiment(num_tests=10, bit_length=20, max_trials=50, B_step=100):
#     """
#     Main experiment
#     - num_tests: number of different N to test
#     - bit_length: bit length for generating prime factors
#     - max_trials: maximum number of trials before giving up
#     """
#     print(f"Number of tests: {num_tests}")
#     print(f"Prime bit length: {bit_length}")
#     print(f"Max trials per method: {max_trials}")
#     print("=" * 70)
#     print()

#     N_values, p_values, q_values = generate_N_sets(num_tests, bit_length)
#     print("N values", N_values)

#     min_N = min(N_values)
#     max_N = max(N_values)
#     min_B = compute_ideal_B(min_N)
#     p_estimate = 2^bit_length
#     max_B = int(p_estimate)

#     B_values = []
#     pell_successes = []
#     pollard_successes = []
#     williams_successes = []
 
#     # Compare success rate for min ideal B till max N
#     for B in range(min_B, max_B, B_step):
#         print(f"B = {B}")
#         B_values.append(B)

#         # Dictionary to store success/failure counts
#         success_counts = {
#             'pell': 0,
#             'pollard': 0,
#             'williams': 0
#         }

#         for test_num in range(1, num_tests + 1):
#             # Generate N
#             N = N_values[test_num-1]
#             p = p_values[test_num-1]
#             q = q_values[test_num-1]

#             print(f"Test {test_num}/{num_tests} started", flush=True)
#             # print(f"N = {N} = {p} * {q}")

#             # Test Pell's method
#             print("  Testing Pell's method")
#             for trial in range(1, max_trials + 1):
#                 result = pell_method(N, B)
#                 if result != "failure":
#                     success_counts['pell'] += 1
#                     print(f"Success on trial {trial}, found factor: {result}")
#                     break
#             else:
#                 print(f"Failed after {max_trials} trials")
            
#             # Test Pollard's method
#             print("  Testing Pollard's method")
#             for trial in range(1, max_trials + 1):
#                 result = pollard_method(N, B)
#                 if result != "failure":
#                     success_counts['pollard'] += 1
#                     print(f"Success on trial {trial}, found factor: {result}")
#                     break
#             else:
#                 print(f"Failed after {max_trials} trials")
            
#             # Test Williams' method
#             print("  Testing Williams' method")
#             for trial in range(1, max_trials + 1):
#                 result = williams_method(N, B)
#                 if result != "failure":
#                     success_counts['williams'] += 1
#                     # print(f"Success on trial {trial}, found factor: {result}")
#                     break
#             else:
#                 print(f"Failed after {max_trials} trials")
        
#         # Print summary statistics
#         print("=" * 70)
#         print(f"\nResults for B value: {B}")

#         for method in ['pell', 'pollard', 'williams']:
#             print(f"\n{method.upper()}'S METHOD:")
#             print(f"  Successes: {success_counts[method]}/{num_tests}")
#         print()
        
#         pell_successes.append(success_counts['pell'])
#         pollard_successes.append(success_counts['pollard'])
#         williams_successes.append(success_counts['williams'])
        
#     print("B values", B)
#     print("Pell successes", pell_successes)
#     print("Pollard successes", pollard_successes)
#     print("Williams successes", williams_successes)

def run_experiment_geom_step(num_tests=10, bit_length=20, max_trials=50, B_mult=1.5):
    """
    Main experiment
    - num_tests: number of different N to test
    - bit_length: bit length for generating prime factors
    - max_trials: maximum number of trials before giving up
    """
    print(f"Number of tests: {num_tests}")
    print(f"Prime bit length: {bit_length}")
    print(f"Max trials per method: {max_trials}")
    print("=" * 70)
    print()

    N_values, p_values, q_values = generate_N_sets(num_tests, bit_length)
    print("N values", N_values)

    min_N = min(N_values)
    max_N = max(N_values)
    # min_B = compute_ideal_B(min_N)
    p_estimate = 2^bit_length
    # Probability of getting p-1 to be B-smooth is u^{-u}
    # With u = 2, u^{-u} = 1/4 which starts to be significant
    # With u = 3, u^{-u} = 0.037 - pretty low
    # With u = 4, u^{-u} = 0.004 - even lower. u higher than 4 makes it almost impossible to succeed
    # To show the difference, we probably start from u = 4 -> B = p^{1/u} = p^{1/4}
    min_B = math.ceil(p_estimate^(1/4))
    max_B = int(p_estimate)

    B_values = []
    pell_successes = []
    pollard_successes = []
    williams_successes = []

    B = min_B  
    # Compare success rate for min ideal B till max N
    while B < max_B:
        print(f"B = {B}")
        B_values.append(B)

        # Dictionary to store success/failure counts
        success_counts = {
            'pell': 0,
            'pollard': 0,
            'williams': 0
        }

        for test_num in range(1, num_tests + 1):
            # Generate N
            N = N_values[test_num-1]
            p = p_values[test_num-1]
            q = q_values[test_num-1]

            print(f"Test {test_num}/{num_tests} started", flush=True)
            # print(f"N = {N} = {p} * {q}")

            # Test Pell's method
            print("  Testing Pell's method")
            for trial in range(1, max_trials + 1):
                result = pell_method(N, B)
                if result != "failure":
                    success_counts['pell'] += 1
                    print(f"Success on trial {trial}, found factor: {result}")
                    break
            else:
                print(f"Failed after {max_trials} trials")
            
            # Test Pollard's method
            print("  Testing Pollard's method")
            for trial in range(1, max_trials + 1):
                result = pollard_method(N, B)
                if result != "failure":
                    success_counts['pollard'] += 1
                    print(f"Success on trial {trial}, found factor: {result}")
                    break
            else:
                print(f"Failed after {max_trials} trials")
            
            # Test Williams' method
            print("  Testing Williams' method")
            for trial in range(1, max_trials + 1):
                result = williams_method(N, B)
                if result != "failure":
                    success_counts['williams'] += 1
                    # print(f"Success on trial {trial}, found factor: {result}")
                    break
            else:
                print(f"Failed after {max_trials} trials")

            print()
        
        # Print summary statistics
        print("=" * 70)
        print(f"\nResults for B value: {B}")

        for method in ['pell', 'pollard', 'williams']:
            print(f"\n{method.upper()}'S METHOD:")
            print(f"  Successes: {success_counts[method]}/{num_tests}")
        print()

        # Update B
        B = math.ceil(B * B_mult)
        
        pell_successes.append(success_counts['pell'])
        pollard_successes.append(success_counts['pollard'])
        williams_successes.append(success_counts['williams'])

    print("B values", B)
    print("Pell successes", pell_successes)
    print("Pollard successes", pollard_successes)
    print("Williams successes", williams_successes)


if __name__ == "__main__":
    results = run_experiment_geom_step(num_tests=1000, bit_length=20, max_trials=50, B_mult=1.5)



