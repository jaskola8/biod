from typing import Callable, List


def main():
    pass


class HtPasswd():

    def __init__(self, filename: str):
        self.data = self._fromfile(filename)

    def write(self, filename: str):
        pass

    def change_password(self, username: str, password: str):
        pass

    def add_user(self, username: str, password: str):
        pass

    def _fromfile(self, filename: str) -> dict:
        pass


def md5sum(filename: str) -> bool:
    pass


def md5compare(filename_first: str, filename_sec: str) -> bool:
    pass


def time_func(function: Callable, **args) -> str:
    pass


def bruteforce_hashes(hash_func: Callable, hashes: List[str], charset: str) -> dict:
    pass


def find_collision(hashed: str, hash_value: str) -> str:
    pass


def compare_jtr():
    pass


if __name__ == "__main__":
    main()

'''TODO
- read htpasswd to object
- write object to htpasswd
- change password in htpasswd
- add user to htpasswd
- md5sum calculate
- timing function
- bruteforce hash
- collisions
'''
