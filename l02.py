import math
import string

from Crypto.Cipher import AES
import hashlib
from Crypto.Random import get_random_bytes

''' TODO
- obliczanie entropii maksymalnej ciągu długości k w alfabecie o wielkości n
- hasło -> klucz
- AES + CBC file encryption
- uniwersalna funkcji do bruteforce entropią
'''

entropy_log_base = 2
chunk_size = 64 * 1024
encoding = 'utf-8'

def main():
    example = 'entropy'
    alphabet_size = len(string.ascii_lowercase)
    filename = "./reftexts/letters/110CYL067.txt"
    print(str(encrypt_with_aes_cbc_mode('Dupa', filename)))
    print('Entropy = ' + str(calc_max_str_entropy(example, alphabet_size)))


def calc_max_str_entropy(text, dict_size):
    return len(text) * math.log(dict_size, entropy_log_base)


def encrypt_with_aes_cbc_mode(key, filename):
    key = key.encode(encoding=encoding)
    byte_key = hashlib.sha256(key).digest()
    iv = get_random_bytes(16)
    encryptor = AES.new(byte_key, AES.MODE_CBC, iv)
    with open(filename, 'rb') as file:
        while True:
            chunk = file.read(chunk_size)
            if len(chunk) == 0:
                break
            elif len(chunk) % 16 != 0:
                chunk += bytes(' ' * (16 - len(chunk) % 16), encoding=encoding)
                by = encryptor.encrypt(chunk)
                print(by)


if __name__ == "__main__":
    main()
