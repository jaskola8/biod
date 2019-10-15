from Crypto.Cipher import AES
import hashlib
from Crypto.Random import get_random_bytes

''' TODO
- obliczanie entropii maksymalnej ciągu długości k w alfabecie o wielkości n
- hasło -> klucz
- AES + CBC file encryption
- uniwersalna funkcji do bruteforce entropią
'''

chunk_size = 64 * 1024
encoding = 'utf-8'


def main():
    filename = "./reftexts/letters/110CYL067.txt"
    print(str(encrypt_with_aes_cbc_mode('Dupa', filename)))


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
