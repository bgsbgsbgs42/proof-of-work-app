# Proof of Work (PoW) System

A simple Python-based implementation of a proof-of-work system that demonstrates the concept of computational work verification through cryptographic hashing.

## Overview

This project implements two command-line utilities:

1. **pow-create**: Generates a proof-of-work string for a given file with a specified difficulty level (number of leading zero bits).
2. **pow-check**: Validates that a proof-of-work header file is valid for a given input file.

The proof-of-work concept is similar to what's used in blockchain technologies like Bitcoin, where computational work must be performed to find a specific value that, when hashed with other data, produces a hash with certain characteristics (in this case, a minimum number of leading zero bits).

## Requirements

- Python 3.6 or higher
- Standard library modules: `hashlib`, `sys`, `time`, `random`, `string`

## Installation

1. Clone the repository or download the source files
2. Make the scripts executable:

```bash
chmod +x pow-create.py pow-check.py test_pow.py
```

## Usage

### Creating a Proof of Work

```bash
./pow-create.py <nbits> <file>
```

- `<nbits>`: The minimum number of leading zero bits required in the resulting hash
- `<file>`: Path to the input file

Example:
```bash
./pow-create.py 20 sample.txt > sample.pow
```

The output will be written in a standard header format with the following fields:
- `File`: The name of the input file
- `Initial-hash`: The SHA-256 hash of the file
- `Proof-of-work`: The generated proof-of-work string
- `Hash`: The SHA-256 hash of the original hash concatenated with the proof-of-work string
- `Leading-zero-bits`: The actual number of leading zero bits in the generated hash
- `Iterations`: The number of attempts needed to find a valid proof-of-work
- `Compute-time`: The time taken to generate the proof-of-work, in seconds

### Checking a Proof of Work

```bash
./pow-check.py <powheader> <file>
```

- `<powheader>`: Path to the header file containing the proof-of-work information
- `<file>`: Path to the original input file

Example:
```bash
./pow-check.py sample.pow sample.txt
```

The output will indicate whether each check passed or failed:
- Initial hash check: Verifies that the file's hash matches the one in the header
- Leading bits check: Verifies that the number of leading zero bits is correct
- PoW hash check: Verifies that the hash in the header matches the computed hash

The final line will be either `pass` or `fail` based on whether all checks passed.

## Testing

A test script is included to verify that the implementation works correctly:

```bash
./test_pow.py
```

This script runs several tests:
1. Basic proof-of-work creation and validation
2. Validation with a wrong file (which should fail)
3. Validation with a modified header (which should fail)

## How It Works

### pow-create

1. Calculates the SHA-256 hash of the input file
2. Generates random 4-character strings as potential proof-of-work values
3. For each potential value, concatenates it with the file's hash and calculates a new SHA-256 hash
4. Counts the number of leading zero bits in this new hash
5. If the number of leading zero bits meets or exceeds the required number, the proof-of-work is valid
6. Outputs the results in the standard header format

### pow-check

1. Parses the header file to extract the proof-of-work information
2. Calculates the SHA-256 hash of the input file and compares it with the `Initial-hash` in the header
3. Concatenates the `Initial-hash` with the `Proof-of-work` string and calculates a new SHA-256 hash
4. Compares this new hash with the `Hash` in the header
5. Counts the number of leading zero bits in the new hash and compares with the `Leading-zero-bits` in the header
6. Outputs `pass` if all checks pass, or `fail` if any check fails

## Verification Examples

You can manually verify the proof-of-work using the `openssl` command:

1. Calculate the SHA-256 hash of the file:
```bash
openssl sha256 < sample.txt
```

2. Concatenate the hash with the proof-of-work string and calculate a new hash:
```bash
echo -n '<hash><pow_string>' | openssl sha256
```

3. Verify that the new hash has the required number of leading zero bits

## Performance Considerations

The difficulty of finding a valid proof-of-work increases exponentially with the number of required leading zero bits. For example:
- 10 bits: ~1,000 iterations (average)
- 20 bits: ~1,000,000 iterations (average)
- 30 bits: ~1,000,000,000 iterations (average)

Choose the difficulty level based on your computational resources and time constraints.

## Applications

Proof-of-work systems have several applications:
- Preventing spam and denial-of-service attacks
- Blockchain consensus mechanisms
- Demonstrating computational effort for various verification purposes
- Cryptographic puzzles and challenges
