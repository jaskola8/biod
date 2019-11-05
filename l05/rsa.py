from typing import Tuple


def keygen() -> Tuple[str, str]:
    pass


def encrypt_RSA(text: str, key: str) -> bytearray:
    pass


def decrypt_RSA(ciphertext: bytearray, key: str) -> str:
    pass


def encrypt_file(in_file: str, out_file: str) -> bool:
    pass
