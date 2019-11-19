import ast
from typing import Tuple
import requests
from Crypto.PublicKey import RSA
from base64 import encodebytes, decodebytes
URL = "http://10.42.11.107:5000"


def keyshare(username):
    rsa_keys = RSA.generate(1024)
    pub_key = rsa_keys.publickey().exportKey()
    r = requests.post(URL+"/key/"+username, json={"message": encodebytes(pub_key).decode('utf-8')})
    if r.status_code == 200:
        print(r.text)
        return rsa_keys
    return None

def get_key(username):
    response = requests.get(URL + "/key/"+username).text
    key = RSA.importKey(decodebytes(response).encode('utf-8'))
    return key

def send_message(msg: str, usr: str):
    key = get_key("michalb2")
    encrypted = key.encrypt(msg.encode(), 32)[0]
    r = requests.post("http://10.42.11.107:5000/message/" + usr, json={"message": encodebytes(encrypted).decode('utf-8')})


if __name__ == "__main__":

    #r = requests.post("http://10.42.11.107:5000/message/michalb2", json={"message": "uno"})
    #print(r.status_code)
    '''
    response = requests.get(URL + "/key/deadbeef").text
    response.encode('utf-8')
    key = RSA.importKey(response)
    message = "dos"
    encrypted = key.encrypt(message.encode(), 32)[0]
    r = requests.post("http://10.42.11.107:5000/message/deadbeef", json={"message": encodebytes(encrypted).decode('utf-8')})
    print(r.text)
    print(r.status_code)'''
    keys = keyshare('michalb2')
    send_message("elo", "michalb2")
    message = decodebytes(requests.get("http://10.42.11.107:5000/message/michalb2").text.encode('utf-8'))
    print(keys.decrypt(message))

