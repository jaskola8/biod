from typing import Tuple


def keygen() -> Tuple[bytearray, bytearray]:
    pass


def encrypt_RSA(text: str, key: bytearray) -> bytearray:
    pass


def decrypt_RSA(ciphertext: bytearray, key: bytearray) -> str:
    pass


def encrypt_file(in_file: str, out_file: str) -> bool:
    pass
