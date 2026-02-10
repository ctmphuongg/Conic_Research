import time
import random
from sage.all import Integer, randint, is_prime, primes
from archived.factor_x_coords import conic_factorization
from archived.p1_algo import p1_factorize_original
from archived.elliptic_curve import ecm_factorization

def generate_test_numbers(num_tests, mode="random", min_size=1000, max_size=10000, max_diff=None):
    """Generate test numbers by multiplying two random primes
    
    Parameters:
    - mode: "random" for random primes, "close" for close primes, "very_close" for extremely close primes
    - max_diff: For close modes, maximum difference between p and q
    """
    test_numbers = []
    prime_pairs = []
    
    for _ in range(num_tests):
        if mode == "random":
            # Generate two random primes
            while True:
                p = randint(min_size, max_size)
                if is_prime(p):
                    break
            while True:
                q = randint(min_size, max_size)
                if is_prime(q):
                    break
        
        elif mode == "close":
            # Generate two close primes
            max_diff = 100 if max_diff is None else max_diff
            while True:
                p = randint(min_size, max_size)
                if is_prime(p):
                    # Look for a prime within max_diff of p
                    for q_candidate in range(p + 1, p + max_diff + 1):
                        if is_prime(q_candidate):
                            q = q_candidate
                            break
                    else:
                        # If no prime found within range, try again
                        continue
                    break
        
        elif mode == "very_close":
            # Generate two extremely close primes
            max_diff = 10 if max_diff is None else max_diff
            while True:
                p = randint(min_size, max_size)
                if is_prime(p):
                    # Look for the closest prime to p
                    for q_candidate in range(p + 1, p + max_diff + 1):
                        if is_prime(q_candidate):
                            q = q_candidate
                            break
                    else:
                        # If no prime found within range, try again
                        continue
                    break
        
        # Multiply them to get our test number
        N = p * q
        test_numbers.append(N)
        prime_pairs.append((p, q))
        
    return test_numbers, prime_pairs

def run_comparison(num_tests=10, test_modes=None, min_size=1000, max_size=10000):
    if test_modes is None:
        test_modes = ["random", "close", "very_close"]
    
    all_results = {}
    
    for mode in test_modes:
        print(f"\n{'='*50}")
        print(f" TESTING MODE: {mode.upper()}")
        print(f"{'='*50}")
        
        # Generate test numbers specific to this mode
        max_diff = 100 if mode == "close" else 10 if mode == "very_close" else None
        test_numbers, prime_pairs = generate_test_numbers(
            num_tests, 
            mode=mode, 
            min_size=min_size, 
            max_size=max_size,
            max_diff=max_diff
        )
        
        results = {
            'conic_p1': {'success': 0, 'total_attempts': 0, 'total_additions': 0, 'avg_attempts': 0, 'avg_additions': 0, 'time': 0},
            'p1_original': {'success': 0, 'total_attempts': 0, 'total_additions': 0, 'avg_attempts': 0, 'avg_additions': 0, 'time': 0},
            'ecm_p1': {'success': 0, 'total_attempts': 0, 'total_additions': 0, 'avg_attempts': 0, 'avg_additions': 0, 'time': 0}
        }
        
        for i, N in enumerate(test_numbers):
            p, q = prime_pairs[i]
            print(f"\nTest {i+1}/{num_tests}")
            print(f"Testing number: {N}")
            print(f"Prime factors: p={p}, q={q}, diff={q-p}")
            
            # Test conic p-1 factorization
            start_time = time.time()
            factor, attempts, additions = conic_factorization(N, method="p-1")
            end_time = time.time()
            results['conic_p1']['total_attempts'] += attempts
            results['conic_p1']['total_additions'] += additions
            results['conic_p1']['time'] += (end_time - start_time)
            
            if factor > 1 and factor < N:
                results['conic_p1']['success'] += 1
                print(f"Conic p-1 found factor: {factor} in {attempts} attempts, {additions} additions, {end_time - start_time:.4f}s")
            else:
                print(f"Conic p-1 failed after {attempts} attempts, {additions} additions, {end_time - start_time:.4f}s")
            
            # Test original p-1 factorization
            start_time = time.time()
            factor, attempts, additions = p1_factorize_original(N)
            end_time = time.time()
            results['p1_original']['total_attempts'] += attempts
            results['p1_original']['total_additions'] += additions
            results['p1_original']['time'] += (end_time - start_time)
            
            if factor > 1 and factor < N:
                results['p1_original']['success'] += 1
                print(f"Original p-1 found factor: {factor} in {attempts} attempts, {additions} additions, {end_time - start_time:.4f}s")
            else:
                print(f"Original p-1 failed after {attempts} attempts, {additions} additions, {end_time - start_time:.4f}s")
            
            # Test ECM p-1 factorization
            start_time = time.time()
            factor, attempts, additions = ecm_factorization(N, method="p-1")
            end_time = time.time()
            results['ecm_p1']['total_attempts'] += attempts
            results['ecm_p1']['total_additions'] += additions
            results['ecm_p1']['time'] += (end_time - start_time)
            
            if factor > 1 and factor < N:
                results['ecm_p1']['success'] += 1
                print(f"ECM p-1 found factor: {factor} in {attempts} attempts, {additions} additions, {end_time - start_time:.4f}s")
            else:
                print(f"ECM p-1 failed after {attempts} attempts, {additions} additions, {end_time - start_time:.4f}s")
        
        # Calculate averages
        for method in results:
            if num_tests > 0:
                results[method]['avg_attempts'] = results[method]['total_attempts'] / num_tests
                results[method]['avg_additions'] = results[method]['total_additions'] / num_tests
                results[method]['avg_time'] = results[method]['time'] / num_tests
        
        # Print summary for this mode
        print(f"\n=== Summary for {mode.upper()} mode ===")
        for method in results:
            print(f"\n{method.upper()} Method:")
            print(f"Success rate: {results[method]['success']}/{num_tests} ({results[method]['success']/num_tests*100 if num_tests > 0 else 0:.2f}%)")
            print(f"Average attempts: {results[method]['avg_attempts']:.2f}")
            print(f"Average additions: {results[method]['avg_additions']:.2f}")
            print(f"Average time: {results[method]['avg_time']:.4f}s")
            print(f"Total attempts: {results[method]['total_attempts']}")
            print(f"Total additions: {results[method]['total_additions']}")
            print(f"Total time: {results[method]['time']:.4f}s")
        
        all_results[mode] = results
    
    # Final comparative analysis across modes
    print("\n\n" + "="*60)
    print(" CROSS-MODE COMPARISON ".center(60, "="))
    print("="*60)
    
    for method in ['conic_p1', 'p1_original', 'ecm_p1']:
        print(f"\n{method.upper()} METHOD ACROSS DIFFERENT PRIME DISTRIBUTIONS:")
        print("-" * 60)
        print(f"{'Mode':<12} {'Success Rate':<15} {'Avg Attempts':<15} {'Avg Additions':<15} {'Avg Time':<10}")
        print("-" * 60)
        
        for mode in all_results:
            success_rate = f"{all_results[mode][method]['success']}/{num_tests} ({all_results[mode][method]['success']/num_tests*100 if num_tests > 0 else 0:.1f}%)"
            print(f"{mode:<12} {success_rate:<15} {all_results[mode][method]['avg_attempts']:<15.2f} {all_results[mode][method]['avg_additions']:<15.2f} {all_results[mode][method]['avg_time']:<10.4f}s")

def run_size_comparison(num_tests=5, size_ranges=None):
    """Run comparisons across different bit sizes"""
    if size_ranges is None:
        size_ranges = [
            (10, 100),     # Very small primes
            (100, 1000),   # Small primes
            (1000, 10000), # Medium primes
            (10000, 100000) # Large primes
        ]
    
    for min_size, max_size in size_ranges:
        print(f"\n\n{'#'*70}")
        print(f"# TESTING SIZE RANGE: {min_size} to {max_size}".ljust(69) + "#")
        print(f"{'#'*70}")
        
        # Run with close primes for this size range
        run_comparison(num_tests=num_tests, test_modes=["close"], min_size=min_size, max_size=max_size)

if __name__ == "__main__":
    # Fix the star in the original code
    # Run standard comparison with different prime distributions
    run_comparison(num_tests=1000, test_modes=["random", "close", "very_close"], min_size=10000, max_size=100000)
    
    # Uncomment to run size comparison
    # run_size_comparison(num_tests=5)