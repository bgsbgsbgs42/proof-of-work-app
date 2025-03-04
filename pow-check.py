#!/usr/bin/env python3
import sys
import hashlib

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

def parse_header_file(header_file):
    """Parse the header file and extract required fields."""
    headers = {}
    
    try:
        with open(header_file, 'r') as file:
            for line in file:
                line = line.strip()
                
                # Skip empty lines
                if not line:
                    continue
                
                # Split by colon and strip spaces
                if ':' in line:
                    key, value = line.split(':', 1)
                    key = key.strip()
                    value = value.strip()
                    headers[key] = value
    except FileNotFoundError:
        print(f"Error: Header file {header_file} not found")
        sys.exit(1)
    
    # Check for required headers
    required_headers = ['Initial-hash', 'Proof-of-work', 'Leading-zero-bits', 'Hash']
    for header in required_headers:
        if header not in headers:
            print(f"ERROR: missing {header} in header")
            return None
    
    return headers

def main():
    if len(sys.argv) != 3:
        print("Usage: pow-check powheader file")
        sys.exit(1)
    
    header_file = sys.argv[1]
    data_file = sys.argv[2]
    
    # Parse header file
    headers = parse_header_file(header_file)
    
    if headers is None:
        print("fail")
        sys.exit(1)
    
    # Read the data file
    try:
        with open(data_file, 'rb') as file:
            file_data = file.read()
    except FileNotFoundError:
        print(f"Error: File {data_file} not found")
        sys.exit(1)
    
    # Compute the initial hash
    actual_initial_hash = compute_sha256(file_data)
    header_initial_hash = headers.get('Initial-hash')
    
    # Check if initial hashes match
    initial_hash_match = actual_initial_hash == header_initial_hash
    if initial_hash_match:
        print("PASSED: initial file hashes match")
    else:
        print("ERROR: initial hashes don't match")
        print(f"   hash in header: {header_initial_hash}")
        print(f"   file hash: {actual_initial_hash}")
    
    # Get proof of work and hash from header
    pow_string = headers.get('Proof-of-work')
    header_hash = headers.get('Hash')
    
    # Compute actual hash using initial hash and proof of work
    combined = header_initial_hash + pow_string
    actual_hash = compute_sha256(combined.encode())
    
    # Check if computed hash matches hash in header
    hash_match = actual_hash == header_hash
    if hash_match:
        print("PASSED: pow hash matches Hash header")
    else:
        print("ERROR: pow hash does not match Hash header")
        print(f"    expected: {actual_hash}")
        print(f"    header has: {header_hash}")
    
    # Check leading zero bits
    header_leading_bits = int(headers.get('Leading-zero-bits'))
    actual_leading_bits = count_leading_zero_bits(actual_hash)
    
    leading_bits_match = header_leading_bits == actual_leading_bits
    if leading_bits_match:
        print("PASSED: leading bits is correct")
    else:
        print(f"ERROR: Leading-zero-bits value: {header_leading_bits}, but hash has {actual_leading_bits} leading zero bits")
    
    # Final result
    if initial_hash_match and hash_match and leading_bits_match:
        print("pass")
    else:
        print("fail")

if __name__ == "__main__":
    main()
