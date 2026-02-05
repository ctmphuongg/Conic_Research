MOD = 143  # Modulus for all operations
import math

def add_elliptic_curve_points(x1, y1, z1, x2, y2, z2):
    """
    Add two points P = (x1 : y1 : z1) and Q = (x2 : y2 : z2) on an elliptic curve
    in projective coordinates, returning R = (x3 : y3 : z3).
    All operations are performed modulo 143.
    
    Note: This assumes Q ≠ ±P and P, Q ≠ O (point at infinity)
    
    Args:
        x1, y1, z1: Projective coordinates of point P
        x2, y2, z2: Projective coordinates of point Q
    
    Returns:
        tuple: (x3, y3, z3) representing the sum R = P + Q (mod 143)
    """
    
    # Calculate temporary values (mod 143)
    U1 = (x1 * z2**2) % MOD
    U2 = (x2 * z1**2) % MOD
    S1 = (y1 * z2**3) % MOD
    S2 = (y2 * z1**3) % MOD
    
    # Calculate intermediate values (mod 143)
    H = (U1 - U2) % MOD
    R = (S1 - S2) % MOD
    G = (H**3) % MOD
    V = (U1 * H**2) % MOD
    
    # Calculate the result coordinates (mod 143)
    x3 = (R**2 + G - 2*V) % MOD
    y3 = (R*(V - x3) - S1*G) % MOD
    z3 = (z1 * z2 * H) % MOD
    
    return (x3, y3, z3)


def double_point(x, y, z, a):
    """
    Double a point P = (x : y : z) on an elliptic curve (point doubling).
    All operations are performed modulo 143.
    
    Args:
        x, y, z: Projective coordinates of point P
        a: Curve parameter 'a' from the elliptic curve equation
    
    Returns:
        tuple: (x3, y3, z3) representing 2P (mod 143)
    """
    
    m = (3*(x**2)+a*(z**4)) % MOD
    t = (y**4)%MOD
    s = (4*x*(y**2))%MOD
    
    x3 = ((m**2)-2*s)%MOD
    y3 = (m*(s-x3)-8*t)%MOD
    z3 = (2*y*z)%MOD
    
    return (x3, y3, z3)


def scalar_multiply(x, y, z, n, a):
    """
    Multiply a point P = (x : y : z) by a scalar n using the double-and-add method.
    This efficiently computes n*P = P + P + ... + P (n times).
    All operations are performed modulo 143.
    
    Args:
        x, y, z: Projective coordinates of point P
        n: Scalar (number of times to add P to itself)
        a: Curve parameter 'a' from the elliptic curve equation
    
    Returns:
        tuple: (x_result, y_result, z_result) representing n*P (mod 143)
    """
    
    if n == 0:
        # Return point at infinity (0 : 1 : 0)
        return (0, 1, 0)
    
    if n == 1:
        return (x, y, z)
    
    # Binary representation of n for double-and-add
    binary = bin(n)[2:]  # Convert to binary string, remove '0b' prefix
    
    # Start with the point P
    result_x, result_y, result_z = x, y, z
    
    # Process each bit from the second bit onward
    for bit in binary[1:]:
        # ALWAYS double the current result
        result_x, result_y, result_z = double_point(result_x, result_y, result_z, a)
        
        # If the bit is 1, add P to the result
        if bit == '1':
            result_x, result_y, result_z = add_elliptic_curve_points(
                result_x, result_y, result_z, x, y, z
            )
    
    return (result_x, result_y, result_z)


# Example usage M=20
if __name__ == "__main__":
    # Test with your parameters
    result = scalar_multiply(3, 4, 1, 2**7, 2)
    print(result)
    print(math.gcd(result[2], MOD))
    result2 = scalar_multiply(result[0], result[1], result[2], 3**5, 2)
    print(result2)
    print(math.gcd(result2[2], MOD))