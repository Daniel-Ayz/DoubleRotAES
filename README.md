# DoubleRotAES

This is an implementation of a DoubleRotAES encryption algorithm.

Let's define the RotAES encryption algorithm as follows:
$RotAESEncrypt(M, k) = AddRoundKey(Rotate(ShiftRows(SubBytes(M))), k) = C$
$RotAESDecrypt(C, k) = SubBytesInv(ShiftRowsInv(RotateInv(AddRoundKey(C, k)))) = M$

The DoubleRotAES encryption algorithm is defined as follows:
$DoubleRotAESEncrypt(M, k1, k2) = RotAESEncrypt(RotAESEncrypt(M, k1), k2) = C$
$DoubleRotAESDecrypt(C, k1, k2) = RotAESDecrypt(RotAESDecrypt(C, k2), k1) = M$

# Example usage

Encrypt using keys K1 K2
```
python aes.py -e message_short.txt keys_short.txt test_cipher_short.txt
```
```
python aes.py -e message_long.txt keys_long.txt test_cipher_long.txt
```
Decrypt using keys K1 K2
```
python aes.py -d cipher_short.txt keys_short.txt test_cipher_short.txt
```
```
python aes.py -d cipher_long.txt keys_long.txt test_cipher_long.txt
```
