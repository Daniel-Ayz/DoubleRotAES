import argparse
import sys

"""
This is an implementation of a DoubleRotAES encryption algorithm.

Let's define the RotAES encryption algorithm as follows:
RotAESEncrypt(M, k) = AddRoundKey(Rotate(ShiftRows(SubBytes(M))), k) = C
RotAESDecrypt(C, k) = SubBytesInv(ShiftRowsInv(RotateInv(AddRoundKey(C, k)))) = M

The DoubleRotAES encryption algorithm is defined as follows:
DoubleRotAESEncrypt(M, k1, k2) = RotAESEncrypt(RotAESEncrypt(M, k1), k2) = C
DoubleRotAESDecrypt(C, k1, k2) = RotAESDecrypt(RotAESDecrypt(C, k2), k1) = M

Assumptions:
M length is a multiple of 16 bytes.
k1 and k2 are 16 bytes long.
"""


s_box = (
    0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,
    0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0,
    0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15,
    0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75,
    0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84,
    0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF,
    0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8,
    0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2,
    0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73,
    0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB,
    0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79,
    0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08,
    0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A,
    0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E,
    0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF,
    0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16,
)

inv_s_box = (
    0x52, 0x09, 0x6A, 0xD5, 0x30, 0x36, 0xA5, 0x38, 0xBF, 0x40, 0xA3, 0x9E, 0x81, 0xF3, 0xD7, 0xFB,
    0x7C, 0xE3, 0x39, 0x82, 0x9B, 0x2F, 0xFF, 0x87, 0x34, 0x8E, 0x43, 0x44, 0xC4, 0xDE, 0xE9, 0xCB,
    0x54, 0x7B, 0x94, 0x32, 0xA6, 0xC2, 0x23, 0x3D, 0xEE, 0x4C, 0x95, 0x0B, 0x42, 0xFA, 0xC3, 0x4E,
    0x08, 0x2E, 0xA1, 0x66, 0x28, 0xD9, 0x24, 0xB2, 0x76, 0x5B, 0xA2, 0x49, 0x6D, 0x8B, 0xD1, 0x25,
    0x72, 0xF8, 0xF6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xD4, 0xA4, 0x5C, 0xCC, 0x5D, 0x65, 0xB6, 0x92,
    0x6C, 0x70, 0x48, 0x50, 0xFD, 0xED, 0xB9, 0xDA, 0x5E, 0x15, 0x46, 0x57, 0xA7, 0x8D, 0x9D, 0x84,
    0x90, 0xD8, 0xAB, 0x00, 0x8C, 0xBC, 0xD3, 0x0A, 0xF7, 0xE4, 0x58, 0x05, 0xB8, 0xB3, 0x45, 0x06,
    0xD0, 0x2C, 0x1E, 0x8F, 0xCA, 0x3F, 0x0F, 0x02, 0xC1, 0xAF, 0xBD, 0x03, 0x01, 0x13, 0x8A, 0x6B,
    0x3A, 0x91, 0x11, 0x41, 0x4F, 0x67, 0xDC, 0xEA, 0x97, 0xF2, 0xCF, 0xCE, 0xF0, 0xB4, 0xE6, 0x73,
    0x96, 0xAC, 0x74, 0x22, 0xE7, 0xAD, 0x35, 0x85, 0xE2, 0xF9, 0x37, 0xE8, 0x1C, 0x75, 0xDF, 0x6E,
    0x47, 0xF1, 0x1A, 0x71, 0x1D, 0x29, 0xC5, 0x89, 0x6F, 0xB7, 0x62, 0x0E, 0xAA, 0x18, 0xBE, 0x1B,
    0xFC, 0x56, 0x3E, 0x4B, 0xC6, 0xD2, 0x79, 0x20, 0x9A, 0xDB, 0xC0, 0xFE, 0x78, 0xCD, 0x5A, 0xF4,
    0x1F, 0xDD, 0xA8, 0x33, 0x88, 0x07, 0xC7, 0x31, 0xB1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xEC, 0x5F,
    0x60, 0x51, 0x7F, 0xA9, 0x19, 0xB5, 0x4A, 0x0D, 0x2D, 0xE5, 0x7A, 0x9F, 0x93, 0xC9, 0x9C, 0xEF,
    0xA0, 0xE0, 0x3B, 0x4D, 0xAE, 0x2A, 0xF5, 0xB0, 0xC8, 0xEB, 0xBB, 0x3C, 0x83, 0x53, 0x99, 0x61,
    0x17, 0x2B, 0x04, 0x7E, 0xBA, 0x77, 0xD6, 0x26, 0xE1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0C, 0x7D,
)


def sub_bytes(state):
    return [s_box[byte] for byte in state]


def sub_bytes_inv(state):
    return [inv_s_box[byte] for byte in state]


# shift rows - each row is shifted to the left by the row number
def shift_rows(state):
    state_matrix = [state[i:i + 4] for i in range(0, len(state), 4)]
    shifted = [state_matrix[row][row:] + state_matrix[row][:row] for row in range(4)]
    return sum(shifted, [])


# inverse shift rows
def shift_rows_inv(state):
    state_matrix = [state[i:i + 4] for i in range(0, len(state), 4)]
    shifted = [state_matrix[row][-row:] + state_matrix[row][:-row] for row in range(4)]
    return sum(shifted, [])


# rotates the matrix 90 degrees clockwise
def rotate(state):
    matrix = [state[i:i+4] for i in range(0, 16, 4)]
    rotated = [list(col) for col in zip(*reversed(matrix))]
    return sum(rotated, [])


def rotate_inv(state):
    # First, form the matrix from the flat list
    matrix = [state[i:i+4] for i in range(0, 16, 4)]
    # Reverse each row first (undo the column reversal from rotate)
    reversed_rows = [row[::-1] for row in matrix]
    # Transpose the matrix (convert rows back to columns to undo the transposition)
    transposed = [list(row) for row in zip(*reversed_rows)]
    # Flatten the matrix back to a list
    return sum(transposed, [])


def add_round_key(state, key):
    return [state[i] ^ key[i] for i in range(len(state))]  # XOR operation


def rot_aes_encrypt(message, key):
    return add_round_key(rotate(shift_rows(sub_bytes(message))), key)


def rot_aes_decrypt(cipher, key):
    return sub_bytes_inv(shift_rows_inv(rotate_inv(add_round_key(cipher, key))))


def double_rot_aes_encrypt(message, key1, key2):
    return rot_aes_encrypt(rot_aes_encrypt(message, key1), key2)


def double_rot_aes_decrypt(cipher, key1, key2):
    return rot_aes_decrypt(rot_aes_decrypt(cipher, key2), key1)


def parse_arguments():
    parser = argparse.ArgumentParser(description='Process DoubleRotAES encryption and decryption.')
    parser.add_argument('-e', '--encrypt', nargs=3, metavar=('MESSAGE_PATH', 'KEY_PATH', 'OUTPUT_PATH'),
                        help='Encrypt the message')
    parser.add_argument('-d', '--decrypt', nargs=3, metavar=('CIPHER_PATH', 'KEY_PATH', 'OUTPUT_PATH'),
                        help='Decrypt the message')
    return parser.parse_args()


def read_file(file_path):
    with open(file_path, 'rb') as file:
        return file.read()


def write_file(file_path, data):
    with open(file_path, 'wb') as file:
        file.write(data)


def encrypt_blocks(data, k1, k2):
    encrypted_data = bytearray()
    for i in range(0, len(data), 16):
        block = data[i:i+16]
        encrypted_data.extend(double_rot_aes_encrypt(block, k1, k2))
    return bytes(encrypted_data)


def decrypt_blocks(data, k1, k2):
    decrypted_data = bytearray()
    for i in range(0, len(data), 16):
        block = data[i:i+16]
        decrypted_data.extend(double_rot_aes_decrypt(block, k1, k2))
    return bytes(decrypted_data)


def test_rotate():
    state = [1, 5, 9, 13, 2, 6, 10, 14, 3, 7, 11, 15, 4, 8, 12, 16]
    rotated = rotate(state)
    assert rotated == [4, 3, 2, 1, 8, 7, 6, 5, 12, 11, 10, 9, 16, 15, 14, 13]
    rotated_inv = rotate_inv(rotated)
    assert rotated_inv == state


def test():
    message = b'Hello, this is a test message.'
    key1 = b'0123456789abcdef'
    key2 = b'fedcba9876543210'
    encrypted = double_rot_aes_encrypt(message, key1, key2)
    decrypted = double_rot_aes_decrypt(encrypted, key1, key2)
    assert message == decrypted
    print('Test passed!')


def main():
    args = parse_arguments()
    if args.encrypt:
        message_path, key_path, output_path = args.encrypt
        message = read_file(message_path)
        key = read_file(key_path)
        k1, k2 = key[:16], key[16:32]
        encrypted = encrypt_blocks(message, k1, k2)
        write_file(output_path, encrypted)
        print(f'Encrypted data written to {output_path}')
    elif args.decrypt:
        cipher_path, key_path, output_path = args.decrypt
        cipher = read_file(cipher_path)
        key = read_file(key_path)
        k1, k2 = key[:16], key[16:32]
        decrypted = decrypt_blocks(cipher, k1, k2)
        write_file(output_path, decrypted)  # Write as text
        print(f'Decrypted data written to {output_path}')
    else:
        print("Invalid command. Use -e for encrypt or -d for decrypt.")
        sys.exit(1)


# test_rotate()

if __name__ == "__main__":
    main()





