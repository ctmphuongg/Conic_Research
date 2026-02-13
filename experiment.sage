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

def run_experiment(num_tests=10, bit_length=20, max_trials=50):
    """
    Main experiment
    - num_tests: number of different N to test
    - bit_length: bit length for generating prime factors
    - max_trials: maximum number of trials before giving up
    """
    # Dictionary to store trial counts for each method
    trial_counts = {
        'pell': [],
        'pollard': [],
        'williams': []
    }
    
    # Dictionary to store success/failure counts
    success_counts = {
        'pell': 0,
        'pollard': 0,
        'williams': 0
    }

    # Dictionary to store the factor found
    result_log = {
        'pell': [],
        'pollard': [],
        'williams': []
    }
    
    print(f"Number of tests: {num_tests}")
    print(f"Prime bit length: {bit_length}")
    print(f"Max trials per method: {max_trials}")
    print("=" * 70)
    print()
    
    for test_num in range(1, num_tests + 1):
        # Generate N
        N, p, q = generate_semiprime(bit_length)
        B = compute_ideal_B(N)
        
        print(f"Test {test_num}/{num_tests}:")
        print(f"N = {N} = {p} * {q}")
        print(f"B = {B}")
        print()
        
        # Test Pell's method
        print("  Testing Pell's method")
        for trial in range(1, max_trials + 1):
            result = pell_method(N, B)
            if result != "failure":
                trial_counts['pell'].append(trial)
                result_log['pell'].append(result)
                success_counts['pell'] += 1
                print(f"Success on trial {trial}, found factor: {result}")
                break
        else:
            result_log['pell'].append(-1)
            print(f"Failed after {max_trials} trials")
        
        # Test Pollard's method
        print("  Testing Pollard's method")
        for trial in range(1, max_trials + 1):
            result = pollard_method(N, B)
            if result != "failure":
                trial_counts['pollard'].append(trial)
                result_log['pollard'].append(result)
                success_counts['pollard'] += 1
                print(f"Success on trial {trial}, found factor: {result}")
                break
        else:
            result_log['pollard'].append(-1)
            print(f"Failed after {max_trials} trials")
        
        # Test Williams' method
        print("  Testing Williams' method")
        for trial in range(1, max_trials + 1):
            result = williams_method(N, B)
            if result != "failure":
                trial_counts['williams'].append(trial)
                result_log['williams'].append(result)
                success_counts['williams'] += 1
                print(f"Success on trial {trial}, found factor: {result}")
                break
        else:
            print(f"Failed after {max_trials} trials")
            result_log['williams'].append(-1)
        
        print()
    
    # Print summary statistics
    print("=" * 70)
    
    for method in ['pell', 'pollard', 'williams']:
        print(f"\n{method.upper()}'S METHOD:")
        print(f"  Successes: {success_counts[method]}/{num_tests}")
        
        if trial_counts[method]:
            trials = trial_counts[method]
            print("Number of trials", trials)
            print("Results", result_log[method])

if __name__ == "__main__":
    results = run_experiment(num_tests=100, bit_length=20, max_trials=50)



