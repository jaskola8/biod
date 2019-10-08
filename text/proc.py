import math
import re


# Calculates entropy of text using frequencies of chars
def calc_text_entropy(text: str):
    freq = calc_char_freq(text)
    prob = create_char_prob(freq)
    result = 0
    for char in text:
        result += prob[char] * math.log(prob[char], 2)
    return -result


# Create char probability dict from frequency dict
def create_char_prob(freq: dict):
    prob = {}
    size = sum(freq.values())
    for k in freq.keys():
        prob[k] = freq[k] / size
    return prob


# Creates char frequency dict
def calc_char_freq(text: str, freq: dict = None):
    new = False
    if freq is None:
        new = True
        freq = {}
    for char in text:
        if char not in freq.keys():
            freq[char] = 1
        else:
            freq[char] += 1
    if new:
        return freq


# Removes whitespaces from text
def remove_whitespaces(text: str):
    pattern = re.compile(r'\s+')
    return re.sub(pattern, '', text)


# Calculates char frequency for file
def create_char_freq_from_file(filepath: str):
    freq = {}
    with open(filepath, 'r') as f:
        for line in f:
            calc_char_freq(remove_whitespaces(line), freq)
    return freq


''' TODO
- select best way to calculate frequency/probability'''