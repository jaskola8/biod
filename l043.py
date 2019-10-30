import ctypes
import multiprocessing
import time

from Crypto.Cipher import DES
from Crypto.Random import get_random_bytes


def xor64(a, b):
    block = bytearray(a, 'utf-8')
    for j in range(8):
        block[j] = ord(a[j]) ^ b[j]
    return block


def xor64bits(a, b):
    block = bytearray(8)
    for j in range(8):
        block[j] = a[j] ^ b[j]
    return block


def encrypt_CBC_serial(key, plain_text, iv):
    vector = bytearray(plain_text, 'utf-8')
    des = DES.new(key)
    for i in range(no_blocks):
        offset = i * block_size
        block = plain_text[offset:offset + block_size]
        intermediate = bytes(xor64(block, iv))
        for j in range(1000):
            encrypted = des.encrypt(intermediate)
            intermediate = encrypted
        vector[offset:offset + block_size] = bytearray(encrypted)
        iv = encrypted
    return bytes(vector)


def decrypt_CBC_serial(key, encrypted_block):
    vector = bytearray(encrypted_block)
    prev_block = encrypted_block[:block_size]
    print(prev_block)
    des = DES.new(key)
    encrypted_block = encrypted_block[block_size:]
    for i in range(no_blocks):
        offset = i * block_size
        block = encrypted_block[offset:offset + block_size]
        for j in range(1000):
            decrypted = des.decrypt(block)
            block = decrypted
        decrypted = xor64bits(block, prev_block)
        vector[offset:offset + block_size] = decrypted
        prev_block = encrypted_block[offset: offset + block_size]
    return bytes(vector)


if __name__ == '__main__':
    plain_text = "alamakot" * 1000
    key = "haslo123"
    iv = get_random_bytes(8)
    block_size = 8
    no_blocks = int(len(plain_text) / block_size)

    starttime = time.time()
    encryptedCBC = encrypt_CBC_serial(key, plain_text, iv)
    print('CBC Encrypt time serial: ', (time.time() - starttime))
    print("Encrypted CBC: ", encryptedCBC)
    starttime = time.time()
    decrypted = decrypt_CBC_serial(key, iv + encryptedCBC)
    print('Decrypted CBC: ' + "".join(map(chr, decrypted)))
    print('CBC Decrypt time serial: ', (time.time() - starttime))


    def mapper(i):
        offset = i * block_size
        prev_block = iv if i == 0 else bytes(shared_data[offset - block_size:offset])
        block = bytes(shared_data[offset:offset + block_size])
        for j in range(1000):
            decrypted = des.decrypt(block)
            block = decrypted
        output_data[offset:offset + block_size] = bytearray(xor64bits(decrypted, prev_block))
        return i


    des = DES.new(key)
    shared_data = multiprocessing.RawArray(ctypes.c_ubyte, encryptedCBC)
    output_data = multiprocessing.RawArray(ctypes.c_ubyte, encryptedCBC)
    pool = multiprocessing.Pool(4)
    starttime = time.time()
    pool.map(mapper, range(no_blocks))
    print('CBC Decrypt time parallel: ', (time.time() - starttime))
    decrypted = bytes(output_data)
    print('Decrypted CBC parallel: ' + "".join(map(chr, decrypted)))
