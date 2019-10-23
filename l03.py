import crypt
import hashlib
import itertools
import random
import string
import subprocess
import timeit
from typing import Callable, List, Dict


# Remember to remove john.pot
def main():
    '''htpasswd = Htpasswd('./resources/htpasswd1')
    #htpasswd.add_user('pip', 'bip')
    #htpasswd.add_user('dick', 'sik')
    #htpasswd.change_password('dick', 'zik')
    #tpasswd.add_user('mick', 'rick')

    htpasswd.write('./resources/htpasswd1')
    print(htpasswd.data)
    print(htpasswd.check_user('admin', 'aaa'))
    print(htpasswd.check_user('pip', 'bip'))
    print(htpasswd.check_user('mick', 'rick'))
    #print(bruteforce_hashes(htpasswd.data.values(), string.ascii_lowercase, 3))
    #print(bruteforce_hashes(htpasswd.data.values(), string.ascii_lowercase, 3))
    htpasswd = Htpasswd('./resources/htpasswd1')
    print(htpasswd.data)
    htpasswd.change_password('mick')
    htpasswd.change_password('pip')
    print(htpasswd.data)
    htpasswd.write('./resources/htpasswd1')
'''
    compare_time()

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

    def change_password(self, username: str):
        if username not in self.data:
            print("Uzytkownik {} nie znajduje sie w bazie.".format(username))
            return False
        passwd = input('Old password: ')
        if self.data[username] == crypt.crypt(passwd, self.data[username]):
            new_passwd = input('New password: ')
            if new_passwd == input('Repeat password: '):
                method = crypt.METHOD_MD5 if self.data[username][0] == '$' else crypt.METHOD_CRYPT
                self.data[username] = crypt.crypt(new_passwd, method)
                return True
            else:
                print("Passwords do not match")
        else:
            print("Wrong password")
        return False


def md5():
    crypt.crypt(''.join(random.choices(string.ascii_lowercase, k=3)), crypt.METHOD_MD5)


def crypting():
    crypt.crypt(''.join(random.choices(string.ascii_lowercase, k=3)), crypt.METHOD_CRYPT)


def compare_time():
    iterations = 5000
    m5time = timeit.timeit(md5, number=5000)
    print('Algorytm MD5: {} hashy na sekundę.', iterations / m5time)
    cryptime = timeit.timeit(crypting, number=5000)
    print('Algorytm crypt: {} hashy na sekundę.', iterations / cryptime)

    def add_user(self, username: str, password: str, method):
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


def md5sum(filename: str) -> str:
    hash_md5 = hashlib.md5()
    with open(filename, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


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


def trivial_hash(dane):
    hash = 0
    for znak in dane:
        hash += ord(znak)
    return hash % 999


if __name__ == "__main__":
    main()

'''TODO
- read htpasswd to object DONE
- write object to htpasswd DONE
- change password in htpasswd DONE

- md5sum compare DONE
- bruteforce hash DONE
- collisions
- compare johntheripper to python DONE
'''
