from text import proc as pr


dict_size = 256  # Size of character set
offset = 0  # Position of first character in set


def main():
    global dict_size
    global offset
    # text = "napis do testowania"
    #text = "###"
    # print(rot(text, 3))
    # print(rot256(rot256(text, 13), 13, True))
    #print(vigenere(vigenere(text, "abcd"), "abcd", True))
    # print(vigenere(text, "###"))

    '''filename = "./reftexts/letters/110CYL067.txt"
    ref_filename = "./reftexts/fiction/A_Wasted_Day.txt"
    with open(filename, "r") as f:
        text = f.read()
    cipher = rot(text, 10)
    decrypt_by_freq(ref_filename, cipher)'''

    key = "Wiki"
    text = "pedia"
    encoded = encode_rc4(text, key)
    print(encoded)
    print(decode_rc4(encoded, key))


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


def decrypt_by_freq(ref_file, text):
    ref_prob = pr.create_char_prob(pr.create_char_freq_from_file(ref_file))
    best_guess = {}
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
          "z odszyfrowanym tekstem postaci: {}\n".format(best_fit, best_guess_dis, best_guess))


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
        result += "%02X" % (ord(c) ^ next(key))

    return result


def decode_rc4(text: str, k: str):
    return bytearray.fromhex(encode_rc4(bytearray.fromhex(text).decode("Latin-1"), k)).decode()


def PRGA(S):
    i, j = 0, 0
    while True:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]  # swap

        K = S[(S[i] + S[j]) % 256]
        yield K



''' TODO
- plot char freq for comparison
- RC4
- bruteforce with entropy
'''


if __name__ == "__main__":
    main()
