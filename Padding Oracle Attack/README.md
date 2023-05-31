# Padding Oracle Attack

This code is an implementation of a Padding Oracle Attack. The attack exploits a vulnerability in systems that use padding for encryption to extract sensitive information from encrypted data. It manipulates the padding and analyzes responses from an oracle to achieve its goal.

## Usage

- Python 3.x
- Dependencies: Cryptodome library (`pip install pycryptodome`)

## How to Run

1. Save the code in a file named `padding_oracle_attack.py`.
2. Open a terminal or command prompt.
3. Navigate to the directory containing the file.
4. Run the script using: `python padding_oracle_attack.py <ciphertext> <key> <iv>`, replacing `<ciphertext>`, `<key>`, and `<iv>` with the appropriate values.

## Code Description

- `xor(a, b, c)`: Calculates the XOR of three values `a`, `b`, and `c`.
- `des_unpad(ciphertext, key, iv)`: Decrypts the ciphertext using DES algorithm with the given key and IV, and removes the padding.
- `oracle(ciphertext, key, iv)`: Checks if the padding of the ciphertext is valid using `des_unpad`.
- `change_and_send(c, key, iv, i)`: Modifies the i-th byte of ciphertext, increments it, and checks if the resulting padding is valid.
- `block_decription(prev_blk, cur_blk, key, iv)`: Decrypts each byte of the current block by manipulating padding and extracts the original byte values.
- `block_loop(blocks, key, iv)`: Decrypts each block of ciphertext in reverse order by calling `block_decription`.
- `initialize(ciphertext, iv)`: Splits the ciphertext into DES block-size blocks by adding the IV.
- `convert_input(argv)`: Converts command-line arguments into the required format.
- `main()`: Handles command-line arguments, performs the padding oracle attack, and prints the decrypted plaintext.

## Example

To execute the code, use the following command:

```
python padding_oracle_attack.py <ciphertext> <key> <iv>
```

Replace `<ciphertext>`, `<key>`, and `<iv>` with appropriate values. The decrypted plaintext will be printed as the output.

**Note:** Ensure the Cryptodome library is installed before running the code.
