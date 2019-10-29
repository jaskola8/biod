import crypt
import itertools
import string
import subprocess
import timeit
import hashlib
from typing import Callable, List, Dict


def main():
    htpasswd = Htpasswd('./resources/htpasswd')
    htpasswd.add_user('pip', 'bip')
    htpasswd.add_user('ugh', 'sik')
    htpasswd.change_password('ugh', 'zik')
    htpasswd.write('./resources/htpasswd')
    print(htpasswd.data)
    print(htpasswd.check_user('pip', 'bip'))

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
        self.data[username] = crypt.crypt(password, crypt.METHOD_MD5)

    def check_user(self, username: str, password: str):
        if self.data.__contains__(username):
            return self.data[username] == crypt.crypt(password, self.data[username])
        return False

    @staticmethod
    def _fromfile(filename: str) -> Dict[str, str]:
        data = {}
        with open(filename, 'r') as f:
            for line in f:
                user, passwd = line.strip().split(':')
                data[user] = passwd
        return data


if __name__ == "__main__":
    main()