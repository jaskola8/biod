import hashlib
import itertools
import math
import string

from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes
from PIL import Image

from BMPencrypt import convert_to_RGB
from BMPencrypt import encrypt
from BMPencrypt import expand_data
from text import proc as pr

ENTROPY_LIMIT = 5
chunk_size = 64 * 1024
encoding = 'utf-8'
entropy_log_base = 2

''' TODO
- obliczanie entropii maksymalnej ciągu długości k w alfabecie o wielkości n
- hasło -> klucz
- AES + CBC file encryption
- uniwersalna funkcji do bruteforce entropią
'''

def main():
    '''
    print(keygen("janusz","safgasga", 4096, 256))
    rc4_cipher = "./crypto.rc4"
    with open(rc4_cipher, "rb") as f:
        text = f.read()

    decoded, key = bruteforce(text, ARC4, 3, string.ascii_lowercase)
    print(key)
    print(decoded)
    '''

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


def zad1():
    cbc_filename = encrypt("./resources/demo24.bmp", "CBC", "key4567890123456")
    ecb_filename = encrypt("./resources/demo24.bmp", "ECB", "key4567890123456")
    with open(cbc_filename, "rb", ) as f:
        print(pr.calc_text_entropy(f.read()))
    with open(ecb_filename, "rb", ) as f:
        print(pr.calc_text_entropy(f.read()))


def zad2():
    salt = "aaaaaaaaaaaaaaaa"
    input_filename = './resources/we800_CBC_encrypted.bmp'
    img_in = Image.open(input_filename)
    data = img_in.convert("RGB").tobytes()
    entropy = 99
    data_expanded = expand_data(data)
    passing = True
    for passwd in itertools.product(string.ascii_lowercase, repeat=3):
        passwd = ''.join(passwd)
        if passwd == "fea":
            passing = False
        if passing:
            continue
        print(passwd)
        key = PBKDF2(passwd, b'abc')
        aes = AES.new(key, AES.MODE_CBC, salt)
        decoded = convert_to_RGB(aes.decrypt(data_expanded)[:len(data)])
        entropy = pr.calc_text_entropy(decoded)
        if entropy < ENTROPY_LIMIT:
            img_out = Image.new(img_in.mode, img_in.size)
            img_out.putdata(decoded)
            output_filename = './resources/decrypted.bmp'
            img_format = str(input_filename.split('.')[-1])
            img_out.save(output_filename, img_format)
            return entropy


if __name__ == "__main__":
    # zad1()
    print(zad2())
