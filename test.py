import unittest

# Assuming encryption functions are imported from another module named encryption
from aes import sub_bytes, sub_bytes_inv, shift_rows, shift_rows_inv, rotate, rotate_inv, add_round_key, s_box, inv_s_box
from aes import rot_aes_encrypt, rot_aes_decrypt, double_rot_aes_encrypt, double_rot_aes_decrypt


"""
Example manual tests:
python aes.py -e message_short.txt keys_short.txt test_cipher_short.txt
python aes.py -e message_long.txt keys_long.txt test_cipher_long.txt
python aes.py -d cipher_short.txt keys_short.txt test_cipher_short.txt
python aes.py -d cipher_long.txt keys_long.txt test_cipher_long.txt
"""

class TestEncryptionMethods(unittest.TestCase):

    def test_sub_bytes(self):
        state = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
        expected = [s_box[b] for b in state]
        self.assertEqual(sub_bytes(state), expected, "sub_bytes does not match expected output")

    def test_sub_bytes_inv(self):
        state = [i for i in range(16)]
        expected = [inv_s_box[b] for b in range(16)]
        self.assertEqual(sub_bytes_inv(state), expected, "sub_bytes_inv does not reverse sub_bytes")

    def test_shift_rows(self):
        state = [i for i in range(16)]
        expected = [0, 1, 2, 3, 5, 6, 7, 4, 10, 11, 8, 9, 15, 12, 13, 14]
        self.assertEqual(shift_rows(state), expected, "shift_rows does not match expected output")

    def test_shift_rows_inv(self):
        state = [0, 1, 2, 3, 5, 6, 7, 4, 10, 11, 8, 9, 15, 12, 13, 14]
        expected = [i for i in range(16)]
        self.assertEqual(shift_rows_inv(state), expected, "shift_rows_inv does not reverse shift_rows")

    def test_rotate(self):
        state = [i for i in range(16)]
        expected = [12, 8, 4, 0, 13, 9, 5, 1, 14, 10, 6, 2, 15, 11, 7, 3]
        self.assertEqual(rotate(state), expected, "rotate does not match expected output")

    def test_rotate_inv(self):
        state = [12, 8, 4, 0, 13, 9, 5, 1, 14, 10, 6, 2, 15, 11, 7, 3]
        expected = [i for i in range(16)]
        self.assertEqual(rotate_inv(state), expected, "rotate_inv does not reverse rotate")

    def test_add_round_key(self):
        state = [i for i in range(16)]
        key = [1]*16
        expected = [i ^ 1 for i in range(16)]
        self.assertEqual(add_round_key(state, key), expected, "add_round_key does not match expected output")

    def test_double_rot_aes(self):
        message = [i for i in range(16)]
        key1 = [2]*16
        key2 = [3]*16
        encrypted = double_rot_aes_encrypt(message, key1, key2)
        decrypted = double_rot_aes_decrypt(encrypted, key1, key2)
        self.assertEqual(decrypted, message, "double_rot_aes encryption and decryption do not match")

    def test_rot_aes(self):
        message = [i for i in range(16)]
        key = [2]*16
        encrypted = rot_aes_encrypt(message, key)
        decrypted = rot_aes_decrypt(encrypted, key)
        self.assertEqual(decrypted, message, "rot_aes encryption and decryption do not match")


if __name__ == '__main__':
    unittest.main()
