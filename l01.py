
from text import proc as pr
import matplotlib.pyplot as plt
import binascii
import itertools
import string

import matplotlib.pyplot as plt
from Crypto.Cipher import ARC4

from text import proc as pr

dict_size = 256  # Size of character set
offset = 0  # Position of first character in set


def main():
    global dict_size
    global offset
    # text = "napis do testowania"
    # text = "###"
    # print(rot(text, 3))
    # print(rot256(rot256(text, 13), 13, True))
    # print(vigenere(vigenere(text, "abcd"), "abcd", True))
    # print(vigenere(text, "###"))

    filename = "./reftexts/letters/110CYL067.txt"
    ref_filename = "./reftexts/fiction/A_Wasted_Day.txt"

    ref_rafalala_pl = "./reftexts/languages/rafalalapl.txt"
    ref_rafalala_eng = "./reftexts/languages/rafalalaeng.txt"
    ref_rafalala_de = "./reftexts/languages/rafalalade.txt"

    create_freq_histogram(pr.create_char_freq_from_file(ref_rafalala_pl))
    create_freq_histogram(pr.create_char_freq_from_file(ref_rafalala_de))
    create_freq_histogram(pr.create_char_freq_from_file(ref_rafalala_eng))

    with open(filename, "r") as f:
    '''
    rot_cipher = "./crypto.rot"
    ref_filename = "./reftexts/fiction/A_Wasted_Day.txt"
    with open(rot_cipher, "r") as f:
        decrypt_by_freq(ref_filename, f.read())

    for filename in (ref_filename, "./example.pl"):
        with open(filename, "r") as f:
            freq = pr.calc_char_freq(f.read())
            create_freq_histogram(freq)
    '''
    rc4_cipher = "./crypto.rc4"
    with open(rc4_cipher, "rb") as f:
        text = f.read()

    key, fit, decoded = bruteforce_RC4(text, 3)
    print(key, fit)
    print(decoded)



# Encrypt/Decrypt given text by rotation
def rot(text: str, distance: int, reverse=False):
    distance *= -1 if reverse else 1
    result = ""
    for char in text:
        result += chr(((ord(char) + distance - offset) % dict_size) + offset)
    return result


# Encrypt/Decrypt given text by Vigenere cipher using keyword
def vigenere(text: str, keyword: str, decrypt=False):
    result = ""
    for index, char in enumerate(text):
        result += rot(char, ord(keyword[index % len(keyword)]) - offset, decrypt)
    return result


# Decrypt rotational ciphertexts by analizing frequency
def decrypt_by_freq(ref_file, text):
    ref_prob = pr.create_char_prob(pr.create_char_freq_from_file(ref_file))
    best_guess = ""
    best_guess_dis = None
    best_fit = -1
    for dis in range(0, dict_size):
        guess = ""
        fit = 0
        rotated_text = rot(text, dis)
        prob = pr.calc_char_freq(rotated_text)
        for k in prob.keys():
            if k in ref_prob.keys():
                fit += abs(prob[k] - ref_prob[k]) * ref_prob[k]
        if round(fit, 5) > best_fit:
            best_fit = fit
            best_guess = rotated_text
            best_guess_dis = dis
    print("Najlepsze dopasowanie o wartości {} uzyskano stosując przesunięcie o {} pozycji "
          "z odszyfrowanym tekstem postaci: {}\n".format(best_fit, abs(256 - best_guess_dis), best_guess))
    # return best_guess


# Encodes text using rc4 alg and key
def encode_rc4(text: str, k: str):
    result = ''
    S = [x for x in range(256)]
    j = 0
    for i in range(256):
        j = (j + S[i] + ord(k[i % len(k)])) % 256
        S[i], S[j] = S[j], S[i]

    text_num = [ord(c) for c in k]
    key = PRGA(S)
    for c in text:
        result += "%02X" % (c ^ next(key))

    return bytes.fromhex(result).decode("Latin-1")


# Decodes rc4 ciphertext to ascii
def decode_rc4(text: str, k: str):
    text = binascii.hexlify(text)
    print(text)
    return bytearray.fromhex(encode_rc4(bytearray.fromhex(text).decode("Latin-1"), k)).decode()


# Pseudo-random generation algorithm
def PRGA(S):
    i, j = 0, 0
    while True:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]  # swap

        K = S[(S[i] + S[j]) % 256]
        yield K


def bruteforce_RC4(text, key_len):
    lowest_entropy = None
    best_key = ""
    result = ""
    for key in itertools.product(string.ascii_lowercase, repeat=key_len):
        key = ''.join(key)
        cipher = ARC4.new(key)
        decoded = cipher.decrypt(text)
        decoded = bytearray(decoded).decode("Latin-1")
        ent = pr.calc_text_entropy(decoded)
        if lowest_entropy is None or ent < lowest_entropy:
            lowest_entropy = ent
            best_key = key
            result = decoded
    return best_key, lowest_entropy, result


def create_freq_histogram(freq_dict: dict):
    plt.bar(list(freq_dict.keys()), freq_dict.values())
    plt.show()

def create_freq_histogram(freq_dict: dict):
    plt.bar(list(freq_dict.keys()), freq_dict.values())
    plt.show()


''' TODO
- plot char freq for comparison
- improve RC4 (questionable) and implement RC4 bruteforce (easy)
'''

if __name__ == "__main__":
    main()
