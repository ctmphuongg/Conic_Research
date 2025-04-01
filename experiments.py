import time
import random
from sage.all import Integer, randint, is_prime, primes
from factor_x_coords import conic_factorization
from p1_algo import p1_factorize_original
from elliptic_curve import ecm_factorization

def generate_test_numbers(num_tests, min_size=1000, max_size=10000):
    """Generate test numbers by multiplying two random primes"""
    test_numbers = []
    for _ in range(num_tests):
        # Generate two random primes
        while True:
            p = randint(min_size, max_size)
            if is_prime(p):
                break
        while True:
            q = randint(min_size, max_size)
            if is_prime(q):
                break
        # Multiply them to get our test number
        N = p * q
        test_numbers.append(N)
    return test_numbers

def run_comparison(num_tests=10, min_size=1000, max_size=10000):
    test_numbers = generate_test_numbers(num_tests, min_size, max_size)
    
    results = {
        'conic_p1': {'success': 0, 'total_attempts': 0, 'total_additions': 0, 'avg_attempts': 0, 'avg_additions': 0},
        'p1_original': {'success': 0, 'total_attempts': 0, 'total_additions': 0, 'avg_attempts': 0, 'avg_additions': 0},
        'ecm_p1': {'success': 0, 'total_attempts': 0, 'total_additions': 0, 'avg_attempts': 0, 'avg_additions': 0}
    }
    
    for i, N in enumerate(test_numbers):
        print(f"\nTest {i+1}/{num_tests}")
        print(f"Testing number: {N}")
        
        # Generate a random bound B for this test
        B = random.randint(1, N)
        print(f"Using bound B = {B}")
        
        # Test conic p-1 factorization
        factor, attempts, additions = conic_factorization(N, method="p-1", B=B)
        results['conic_p1']['total_attempts'] += attempts
        results['conic_p1']['total_additions'] += additions
        if factor != N:
            results['conic_p1']['success'] += 1
            print(f"Conic p-1 found factor: {factor} in {attempts} attempts and {additions} additions")
        
        # Test original p-1 factorization
        factor, attempts, additions = p1_factorize_original(N, B=B)
        results['p1_original']['total_attempts'] += attempts
        results['p1_original']['total_additions'] += additions
        if factor != N:
            results['p1_original']['success'] += 1
            print(f"Original p-1 found factor: {factor} in {attempts} attempts and {additions} additions")
        
        # Test ECM p-1 factorization
        factor, attempts, additions = ecm_factorization(N, method="p-1", B=B)
        results['ecm_p1']['total_attempts'] += attempts
        results['ecm_p1']['total_additions'] += additions
        if factor != N:
            results['ecm_p1']['success'] += 1
            print(f"ECM p-1 found factor: {factor} in {attempts} attempts and {additions} additions")
    
    # Calculate averages
    for method in results:
        results[method]['avg_attempts'] = results[method]['total_attempts'] / num_tests
        results[method]['avg_additions'] = results[method]['total_additions'] / num_tests
    
    # Print summary
    print("\n=== Summary ===")
    for method in results:
        print(f"\n{method.upper()} Method:")
        print(f"Success rate: {results[method]['success']}/{num_tests} ({results[method]['success']/num_tests*100:.2f}%)")
        print(f"Average attempts: {results[method]['avg_attempts']:.2f}")
        print(f"Average additions: {results[method]['avg_additions']:.2f}")
        print(f"Total attempts: {results[method]['total_attempts']}")
        print(f"Total additions: {results[method]['total_additions']}")

if __name__ == "__main__":
    # Run comparison with 10 test numbers between 1000 and 10000
    run_comparison(num_tests=100, min_size=1000, max_size=10000) 