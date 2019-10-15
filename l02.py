import math
import string

''' TODO
- obliczanie entropii maksymalnej ciągu długości k w alfabecie o wielkości n
- hasło -> klucz
- AES + CBC file encryption
- uniwersalna funkcji do bruteforce entropią
'''

entropy_log_base = 2


def main():
    print('Entropy = ' + str(calc_max_str_entropy("Entropy", len(string.ascii_lowercase))))


def calc_max_str_entropy(text, dict_size):
    return len(text) * math.log(dict_size, entropy_log_base)


if __name__ == "__main__":
    main()
