import math
import random
import matplotlib.pyplot as plt
import numpy as np
import time
from collections import defaultdict
from sage.all import IntegerModRing, IntegerRing, gcd
from add_point_n_times import self_add_optimized, add_point

def find_factor(N, x, y, delta):
    # print(x, y, delta)
    mult = 1
    R = IntegerModRing(N)
    B = math.floor(N**(mult/6))
    M = 1
    for p in range(2, B+1):
        if is_prime(p):
            power = math.floor(math.log(B, p))
            M *= (p**power)

    x1, y1 = self_add_optimized(M, x, y, delta, R)
    # print(x1, y1)
    Z = IntegerRing()
    x1 = Z(x1)
    y1 = Z(y1)
    first_div = gcd(x1-1, N)
    if 1 < first_div < N:
        return first_div
    sec_div = gcd(y1, N)
    if 1 < sec_div < N:
        return sec_div

    return N 

def factorization(N, method="fact", max_attempts=5):
    """
    Factorize N using elliptic curve method
    
    Args:
        N: Number to factorize
        method: "fact" or "p-1" factorization method
        max_attempts: Maximum number of generation attempts
    
    Returns:
        Tuple of (factor, attempts, runtime) where factor is a non-trivial factor of N (or N if not found),
        attempts is the number of generation attempts made, and runtime is the execution time in seconds
    """
    start_time = time.time()
    delta = 2
    
    for attempt in range(1, max_attempts + 1):
        i = random.randint(1, 5)
        x = int(((3 + 2*math.sqrt(2))**i + (3 + 2*math.sqrt(2))**i) / 2) % N
        y = int(((3 + 2*math.sqrt(2))**i + (3 + 2*math.sqrt(2))**i) / (2*math.sqrt(2))) % N
        
        if method == "p-1":
            # Call p-1 factor-finding method
            factor = find_factor(N, x, y, delta)
            if 1 < factor < N:
                end_time = time.time()
                return factor, attempt, end_time - start_time
        else:
            # fact method
            M = min(random.randint(1, N), 1000)  # Limit M for performance
            P = (x, y)
            R = IntegerModRing(N)
            
            for B in range(1, M):
                g = gcd(P[0]-1, N)
                if 1 < g < N:  # Check for non-trivial factor
                    end_time = time.time()
                    return g, attempt, end_time - start_time
                P = self_add_optimized(B, P[0], P[1], delta, R)
    
    end_time = time.time()
    return N, max_attempts, end_time - start_time

def benchmark_factorization(num_samples=100, max_value=10000000, max_attempts=3):
    """
    Benchmark both factorization methods on random numbers
    
    Args:
        num_samples: Number of random samples to test
        max_value: Maximum value for random numbers
        max_attempts: Maximum attempts per factorization
        
    Returns:
        Dictionary containing benchmark results
    """
    # Generate random numbers for testing (exclude primes for more interesting results)
    numbers = []
    while len(numbers) < num_samples:
        n = random.randint(100, max_value)
        if not is_prime(n):
            numbers.append(n)
    
    # Prepare result containers
    results = {
        "fact": {
            "times": [],
            "attempts": [],
            "success_rate": 0,
            "factors_found": [],
            "numbers": []
        },
        "p-1": {
            "times": [],
            "attempts": [],
            "success_rate": 0,
            "factors_found": [],
            "numbers": []
        }
    }
    
    # Store size categories for analysis
    size_categories = defaultdict(lambda: {"fact": [], "p-1": []})
    
    # Run benchmarks
    print(f"Running benchmark on {num_samples} random numbers...")
    
    for i, N in enumerate(numbers):
        size_category = int(math.log10(N))
        
        print(f"Testing number {i+1}/{num_samples}: {N}")
        
        # Test fact method
        factor_std, attempts_std, time_std = factorization(N, method="fact", max_attempts=max_attempts)
        success_std = factor_std != N
        
        # Test p-1 method
        factor_p1, attempts_p1, time_p1 = factorization(N, method="p-1", max_attempts=max_attempts)
        success_p1 = factor_p1 != N
        
        # Store results
        results["fact"]["times"].append(time_std)
        results["fact"]["attempts"].append(attempts_std)
        results["fact"]["factors_found"].append(factor_std if success_std else None)
        results["fact"]["numbers"].append(N)
        
        results["p-1"]["times"].append(time_p1)
        results["p-1"]["attempts"].append(attempts_p1)
        results["p-1"]["factors_found"].append(factor_p1 if success_p1 else None)
        results["p-1"]["numbers"].append(N)
        
        # Store by size category
        size_categories[size_category]["fact"].append(time_std)
        size_categories[size_category]["p-1"].append(time_p1)
    
    # Calculate success rates
    results["fact"]["success_rate"] = sum(1 for f in results["fact"]["factors_found"] if f is not None) / num_samples
    results["p-1"]["success_rate"] = sum(1 for f in results["p-1"]["factors_found"] if f is not None) / num_samples
    
    # Calculate average times by size category
    avg_times_by_size = {
        "categories": [],
        "fact": [],
        "p-1": []
    }
    
    for size, data in sorted(size_categories.items()):
        if data["fact"] and data["p-1"]:
            avg_times_by_size["categories"].append(f"10^{size}")
            avg_times_by_size["fact"].append(np.mean(data["fact"]))
            avg_times_by_size["p-1"].append(np.mean(data["p-1"]))
    
    results["avg_times_by_size"] = avg_times_by_size
    
    return results

def print_stats(results):
    """Print statistics from benchmark results"""
    methods = ["fact", "p-1"]
    
    print("\n===== Factorization Methods Benchmark Results =====")
    
    for method in methods:
        data = results[method]
        print(f"\n--- {method.capitalize()} Method ---")
        print(f"Average runtime: {np.mean(data['times']):.6f} seconds")
        print(f"Median runtime: {np.median(data['times']):.6f} seconds")
        print(f"Max runtime: {np.max(data['times']):.6f} seconds")
        print(f"Min runtime: {np.min(data['times']):.6f} seconds")
        print(f"Success rate: {data['success_rate']*100:.2f}%")
        print(f"Average attempts: {np.mean(data['attempts']):.2f}")
    
    # Print performance comparison
    std_times = np.array(results["fact"]["times"])
    p1_times = np.array(results["p-1"]["times"])
    
    print("\n--- Performance Comparison ---")
    print(f"P-1 method is {np.mean(std_times/p1_times):.2f}x faster on average")
    print(f"P-1 method wins in {np.sum(p1_times < std_times)} out of {len(std_times)} cases ({np.sum(p1_times < std_times)/len(std_times)*100:.2f}%)")

def visualize_results(results):
    """Generate visualizations for benchmark results"""
    # Setup
    plt.figure(figsize=(15, 10))
    
    # 1. Runtime comparison
    plt.subplot(2, 2, 1)
    plt.hist(results["fact"]["times"], alpha=0.5, label="fact Method")
    plt.hist(results["p-1"]["times"], alpha=0.5, label="P-1 Method")
    plt.xlabel("Runtime (seconds)")
    plt.ylabel("Frequency")
    plt.title("Runtime Distribution")
    plt.legend()
    
    # 2. Size vs. runtime
    plt.subplot(2, 2, 2)
    
    # Plot by size categories
    x = range(len(results["avg_times_by_size"]["categories"]))
    plt.bar(
        [i - 0.2 for i in x], 
        results["avg_times_by_size"]["fact"], 
        width=0.4, 
        label="fact Method"
    )
    plt.bar(
        [i + 0.2 for i in x], 
        results["avg_times_by_size"]["p-1"], 
        width=0.4, 
        label="P-1 Method"
    )
    plt.xticks(x, results["avg_times_by_size"]["categories"])
    plt.xlabel("Number Size")
    plt.ylabel("Average Runtime (seconds)")
    plt.title("Runtime by Number Size")
    plt.legend()
    
    # 3. Success rate comparison
    plt.subplot(2, 2, 3)
    plt.bar(
        ["fact", "P-1"],
        [results["fact"]["success_rate"], results["p-1"]["success_rate"]],
        color=["blue", "orange"]
    )
    plt.ylim(0, 1)
    plt.ylabel("Success Rate")
    plt.title("Factor Finding Success Rate")
    
    # 4. Attempts distribution
    plt.subplot(2, 2, 4)
    attempts_std = np.array(results["fact"]["attempts"])
    attempts_p1 = np.array(results["p-1"]["attempts"])
    
    unique_attempts = sorted(set(attempts_std) | set(attempts_p1))
    
    std_counts = [np.sum(attempts_std == att) for att in unique_attempts]
    p1_counts = [np.sum(attempts_p1 == att) for att in unique_attempts]
    
    x = range(len(unique_attempts))
    plt.bar([i - 0.2 for i in x], std_counts, width=0.4, label="fact Method")
    plt.bar([i + 0.2 for i in x], p1_counts, width=0.4, label="P-1 Method")
    plt.xticks(x, unique_attempts)
    plt.xlabel("Number of Attempts")
    plt.ylabel("Frequency")
    plt.title("Attempts Distribution")
    plt.legend()
    
    plt.tight_layout()
    plt.savefig("factorization_benchmark_results.png")
    print("\nVisualization saved as 'factorization_benchmark_results.png'")

if __name__ == "__main__":
    # Set parameters
    NUM_SAMPLES = 50  # Reduced for demonstration, increase for more accurate results
    MAX_VALUE = 10000000
    MAX_ATTEMPTS = 5
    
    print(f"Starting benchmark with {NUM_SAMPLES} random numbers up to {MAX_VALUE}...")
    
    # Run benchmark
    results = benchmark_factorization(
        num_samples=NUM_SAMPLES,
        max_value=MAX_VALUE,
        max_attempts=MAX_ATTEMPTS
    )
    
    # Print statistics
    print_stats(results)
    
    # Visualize results
    visualize_results(results)
    
    print("\nBenchmark completed!")