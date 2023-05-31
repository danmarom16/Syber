import sys
from Cryptodome.Cipher import DES
from Cryptodome.Util.Padding import pad, unpad

# Function that calculates Xor.
def xor(a, b, c):
    result = (a ^ b) ^ c
    return result

# Unpad a given ciphertext and returns it. Raises Value Error if padding is not valid.
def des_unpad(ciphertext, key, iv):
    cipher = DES.new(key, DES.MODE_CBC, iv)
    return unpad(cipher.decrypt(ciphertext),DES.block_size)

# Asks the oracle if the padding is valid
def oracle(ciphertext, key, iv):
    try:
        des_unpad(ciphertext, key, iv)
        return True
    except ValueError:
        return False

# Change the i'th byte and asks the oracle if the padding is valid.
# When the padding is valid, we know the c[i] value + the value at the plaintext prime (i+1).
def change_and_send(c,  key, iv, i):
    while True:
        if oracle(c, key, iv):
            return c[i]
        else:
            c[i] = c[i] + 1  # Increment the 8th byte of c


# Decript each char of the block.
def block_decription(prev_blk, cur_blk, key, iv):
    res = bytearray([0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0])
    c = bytearray(b'\x00' * 8 + cur_blk)

    for i in range(8):
       # Decript the 7-ith byte in the plaintext block.
       m_byte = change_and_send(c, key, iv, 7-i)                
       res[7-i] = xor(m_byte, (i+1), prev_blk[7-i])                 #d = m_byte ^ (i+1)

       for j in range(i+1):
           c[7-i+j] = xor(i+1, i+2, c[7-i+j])

    return res


# Looping through each block and decripting it. When finish, returns a decrypted plaintext.
def block_loop(blocks, key, iv):
    res = []
    for i in range(len(blocks) - 1, 0, -1):
        res = [block_decription(blocks[i - 1], blocks[i], key, iv)] + res
    result = ''.join(bytearray.decode('utf-8') for bytearray in res)
    result = result.encode('utf-8')
    return  result


# Splits ciphertext into DES block size blocks and returns them.
def initialize(ciphertext, iv):
    ciphertext = iv + ciphertext 
    blocks = [ciphertext[i:i+8] for i in range(0, len(ciphertext), 8)]
    return blocks

# Converts hex-string input into array of bytes that represent values in hex.
def convert_input(argv):
    return bytes.fromhex(argv[1]), argv[2].encode('utf-8'), bytes.fromhex(argv[3])


def main():
    # Convert Input
    ciphertext, key, iv = convert_input(sys.argv)

    # Create blocks
    blocks = initialize(ciphertext, iv)

    # Decrypt Blocks and get padded bytes plaintext
    decrypted_plaintext = block_loop(blocks, key, iv)

    # Get unpadded original plaintext
    original_plaintext = unpad(decrypted_plaintext, DES.block_size).decode()

    # Prints original plaintext
    print(original_plaintext)


if __name__ == "__main__":
    main()


    








