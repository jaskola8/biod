import secrets

TEXT_LEN = 8


def text2vec(text: str, length: int) -> bytearray:
    arr = bytearray()
    arr.extend(map(ord, text))
    pad_len = (length - len(arr) * 8) // 8
    arr.extend(bytearray(pad_len))
    return arr


def vec2text(vec: bytearray) -> str:
    vec = vec[:2 * TEXT_LEN]
    vec.decode('Latin-1')
    return text


def fermant(val: int, acc: int) -> bool:
    for _ in range(acc):
        rand = 1 + secrets.randbelow(val - 1)
        if val % rand == 0:
            return False


def erastotenes(val: int) -> bool:
    sieve = [True for _ in range(val + 1)]
    for x in range(2, val):
        while x * 2 <= val:
            x *= 2
            sieve[x] = False
    return sieve[val]


def bcf(x: int, y: int) -> int:
    while y != 0:
        x, y = y, x % y
    return x


def coprime(x: int, y: int) -> bool:
    return bcf(x, y) == 1


def revmod(val: int, mod: int) -> int:
    for x in range(val):
        if (val * x) % mod == 0:
            return x
    return None


def quickpower(val: int, exp: float) -> float:
    if exp == 0:
        return 1
    elif exp % 2 == 1:
        return val * quickpower(val, (exp - 1) / 2) ** 2
    return quickpower(val, exp / 2) ** 2


if __name__ == '__main__':
    text = "Januszta"
    padded = text2vec(text, 128)
    print(padded)
    print(vec2text(padded))
