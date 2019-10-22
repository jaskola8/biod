import crypt
import itertools
import string
import subprocess
import timeit
from typing import Callable, List, Dict


# Remember to remove john.pot
def main():
    htpasswd = Htpasswd('./resources/htpasswd')
    htpasswd.add_user('pip', 'bip')
    htpasswd.add_user('dick', 'sik')
    htpasswd.change_password('dick', 'zik')
    htpasswd.write('./resources/htpasswd')
    print(htpasswd.data)
    print(bruteforce_hashes(htpasswd.data.values(), string.ascii_lowercase, 3))


#    compare_jtr()


class Htpasswd():
    data: Dict[str, str]
    salt: str

    def __init__(self, filename: str):
        self.data = self._fromfile(filename)

    def write(self, filename: str):
        with open(filename, 'w') as f:
            newline = ''
            for username in self.data.keys():
                f.write("%s%s:%s" % (newline, username, self.data[username]))
                newline = '\n'

    def change_password(self, username: str, password: str):
        self.add_user(username, password)

    def add_user(self, username: str, password: str):
        self.data[username] = crypt.crypt(password, crypt.METHOD_CRYPT)

    @staticmethod
    def _fromfile(filename: str) -> Dict[str, str]:
        data = {}
        with open(filename, 'r') as f:
            for line in f:
                user, passwd = line.strip().split(':')
                data[user] = passwd
        return data


def md5sum(filename: str) -> str:
    pass


def md5compare(filename_first: str, filename_sec: str) -> bool:
    return md5sum(filename_first) == md5sum(filename_sec)


def time_func(function: Callable, **args) -> str:
    pass


def bruteforce_hashes(hashes: List[str], charset: str, pass_len: int) -> Dict[str, str]:
    hashset = set(hashes)
    result = dict()
    left = len(hashset)
    for passwd in itertools.product(charset, repeat=pass_len):
        passwd = ''.join(passwd)
        for hashed in hashset:
            pass_hash = crypt.crypt(passwd, hashed)
            if hashed == pass_hash:
                result[hashed] = passwd
                left -= 1
                hashset.remove(hashed)
                break
        if left == 0:
            break
    return result


def find_collision(hashed: str, hash_value: str) -> str:
    pass


def compare_jtr():
    print(timeit.timeit(_helper1, number=1))
    print(timeit.timeit(_helper2, number=10) / 10)


def _helper1():
    subprocess.run(['john', '--incremental=lower', '--format=crypt', './resources/htpasswd'])


def _helper2():
    htpasswd = Htpasswd('./resources/htpasswd')
    bruteforce_hashes(htpasswd.data.values(), string.ascii_lowercase, 3)


if __name__ == "__main__":
    main()

'''TODO
- read htpasswd to object DONE
- write object to htpasswd DONE
- change password in htpasswd DONE
- add user to htpasswd DONE
- md5sum calculate 
- md5sum compare DONE
- bruteforce hash DONE
- collisions
- compare johntheripper to python DONE
'''
