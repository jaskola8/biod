''' TODO
- obliczanie entropii maksymalnej ciągu długości k w alfabecie o wielkości n
- hasło -> klucz
- AES + CBC file encryption
- uniwersalna funkcji do bruteforce entropią
'''
import hashlib
import itertools
import string

from Crypto.Cipher import ARC4

from text import proc as pr

ENTROPY_LIMIT = 5


def keygen(passwd: str, salt: str, iterc: int, keysize: int):
    passwd = passwd.encode(encoding="Latin-1")
    salt = salt.encode(encoding="Latin-1")
    h = hashlib.new("sha256")
    while iterc > 0:
        h.update(passwd + salt)
        iterc -= 1
    result = h.hexdigest()
    sized = keysize - h.digest_size
    while sized > 0:
        h.update(passwd + salt)
        result += h.hexdigest()
        sized -= h.digest_size
    result = bytearray(result, encoding="Latin-1")[:keysize].decode("Latin-1")
    return result


def bruteforce(crypto: str, decryptor, keylen: int, characters: list):
    decoded = ""
    key = ""
    for k in itertools.product(characters, repeat=keylen):
        key = ''.join(k)
        cipher = decryptor.new(key)
        decoded = cipher.decrypt(crypto)
        decoded = bytearray(decoded).decode("Latin-1")
        if pr.calc_text_entropy(decoded) < ENTROPY_LIMIT:
            return decoded, key
    return None, None


if __name__ == "__main__":
    # print(keygen("janusz","safgasga", 4096, 256))

    rc4_cipher = "./crypto.rc4"
    with open(rc4_cipher, "rb") as f:
        text = f.read()

    decoded, key = bruteforce(text, ARC4, 3, string.ascii_lowercase)
    print(key)
    print(decoded)
