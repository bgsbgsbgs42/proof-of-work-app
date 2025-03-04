#!/usr/bin/env python3
import os
import subprocess
import tempfile
import sys

def run_command(command):
    """Run a command and return its output."""
    process = subprocess.run(command, shell=True, capture_output=True, text=True)
    return process.stdout, process.returncode

def create_test_file(content, filename):
    """Create a test file with given content."""
    with open(filename, 'w') as f:
        f.write(content)
    return filename

def test_pow_create_check():
    """Test pow-create and pow-check together."""
    print("Running tests for pow-create and pow-check")
    print("=" * 50)
    
    # Make sure the scripts are executable
    os.system("chmod +x pow-create.py pow-check.py")
    
    # Create a temporary test file
    test_content = "The time has come, the Walrus said, To talk of many things: Of shoes — and ships — and sealing-wax — Of cabbages — and kings — And why the sea is boiling hot — And whether pigs have wings."
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp:
        temp.write(test_content)
        test_file = temp.name
    
    # Create a temporary header file
    header_file = tempfile.NamedTemporaryFile(delete=False).name
    
    try:
        # Test 1: Basic proof of work creation and validation (with a small nbits for speed)
        print("\nTest 1: Basic proof of work creation and validation")
        nbits = 10  # Small number for faster testing
        
        # Run pow-create
        print(f"Running: ./pow-create.py {nbits} {test_file} > {header_file}")
        output, _ = run_command(f"./pow-create.py {nbits} {test_file} > {header_file}")
        
        # Run pow-check
        print(f"Running: ./pow-check.py {header_file} {test_file}")
        output, returncode = run_command(f"./pow-check.py {header_file} {test_file}")
        print(output)
        
        if "pass" in output.lower() and returncode == 0:
            print("Test 1: PASSED")
        else:
            print("Test 1: FAILED")
        
        # Test 2: Check with wrong file
        print("\nTest 2: Check with wrong file")
        wrong_file = create_test_file("This is a different file content", "wrong_file.txt")
        
        print(f"Running: ./pow-check.py {header_file} {wrong_file}")
        output, _ = run_command(f"./pow-check.py {header_file} {wrong_file}")
        print(output)
        
        if "fail" in output.lower():
            print("Test 2: PASSED")
        else:
            print("Test 2: FAILED")
        
        # Test 3: Modify header file to have wrong leading bits
        print("\nTest 3: Modify header with wrong leading bits")
        modified_header = header_file + ".modified"
        with open(header_file, 'r') as original:
            content = original.read()
            
        # Change Leading-zero-bits to a higher value
        modified_content = content.replace(f"Leading-zero-bits: ", f"Leading-zero-bits: 99")
        
        with open(modified_header, 'w') as modified:
            modified.write(modified_content)
        
        print(f"Running: ./pow-check.py {modified_header} {test_file}")
        output, _ = run_command(f"./pow-check.py {modified_header} {test_file}")
        print(output)
        
        if "fail" in output.lower():
            print("Test 3: PASSED")
        else:
            print("Test 3: FAILED")
            
    finally:
        # Clean up
        if os.path.exists(test_file):
            os.remove(test_file)
        if os.path.exists(header_file):
            os.remove(header_file)
        if os.path.exists(modified_header):
            os.remove(modified_header)
        if os.path.exists("wrong_file.txt"):
            os.remove("wrong_file.txt")

if __name__ == "__main__":
    test_pow_create_check()
