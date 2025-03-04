#!/usr/bin/env python3
import sys
import hashlib
import time
import random
import string

def compute_sha256(data):
    """Compute SHA-256 hash of given data."""
    sha256 = hashlib.sha256()
    sha256.update(data)
    return sha256.hexdigest()

def count_leading_zero_bits(hex_str):
    """Count the number of leading zero bits in a hex string."""
    binary = bin(int(hex_str, 16))[2:].zfill(256)
    count = 0
    for bit in binary:
        if bit == '0':
            count += 1
        else:
            break
    return count

def generate_random_string(length=4):
    """Generate a random string of fixed length."""
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

def create_proof_of_work(initial_hash, target_bits, max_iterations=10000000, length=4):
    """Create a proof of work string that results in a hash with target_bits leading zeros."""
    iterations = 0
    while iterations < max_iterations:
        iterations += 1
        
        # Generate a random proof of work string
        pow_string = generate_random_string(length)
        
        # Concatenate with initial hash and compute new hash
        combined = initial_hash + pow_string
        new_hash = compute_sha256(combined.encode())
        
        # Check if we have enough leading zero bits
        zero_bits = count_leading_zero_bits(new_hash)
        if zero_bits >= target_bits:
            return pow_string, new_hash, zero_bits, iterations
    
    # If we reach here, we couldn't find a suitable proof of work
    raise Exception(f"Could not find proof of work with {target_bits} leading zero bits after {max_iterations} attempts")

def main():
    if len(sys.argv) != 3:
        print("Usage: pow-create nbits file")
        sys.exit(1)
    
    try:
        nbits = int(sys.argv[1])
        filename = sys.argv[2]
    except ValueError:
        print("Error: nbits must be an integer")
        sys.exit(1)
    
    try:
        with open(filename, 'rb') as file:
            file_data = file.read()
    except FileNotFoundError:
        print(f"Error: File {filename} not found")
        sys.exit(1)
    
    # Compute the initial hash
    initial_hash = compute_sha256(file_data)
    
    # Start timing
    start_time = time.time()
    
    # Create proof of work
    try:
        pow_string, pow_hash, leading_bits, iterations = create_proof_of_work(initial_hash, nbits)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
    
    # End timing
    end_time = time.time()
    compute_time = end_time - start_time
    
    # Output results
    print(f"File: {filename}")
    print("")
    print(f"Initial-hash: {initial_hash}")
    print("")
    print(f"Proof-of-work: {pow_string}")
    print("")
    print(f"Hash: {pow_hash}")
    print("")
    print(f"Leading-zero-bits: {leading_bits}")
    print("")
    print(f"Iterations: {iterations}")
    print("")
    print(f"Compute-time: {compute_time:.4f}")

if __name__ == "__main__":
    main()
