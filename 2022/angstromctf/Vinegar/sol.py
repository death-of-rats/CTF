#!/usr/bin/env python3
import pwn
import string
from py import process
import re

alpha = string.ascii_lowercase

def decrypt(msg, key):
    ret = ""
    i = 0
    for c in msg:
        if c in alpha:
            ret += alpha[(alpha.index(c)-alpha.index(key[i])) % len(alpha)]
            i = (i + 1) % len(key)
        else:
            ret += c
    return ret

def extract(cipher):
    key = []
    src = "actf"
    for i in range(4):
        key.append( alpha[(alpha.index(cipher[i])-alpha.index(src[i])) % len(alpha)] )
    return decrypt(cipher, "".join(key))

def search(cipher):
    ph = re.compile('[a-z][a-z][a-z][a-z]{[a-z_]*?}[a-z][a-z][a-z][a-z]')
    prop = ph.search(cipher)
    while prop:
        ans = extract(cipher[prop.start():prop.end()])
        if "fleg" in ans:
            return ans[:-4]
        cipher = cipher[prop.start()+5:]
        prop = ph.search(cipher)

    return ""

#prog = pwn.process('main.py')
prog = pwn.remote('challs.actf.co', 31333)
prog.recvline()

for _ in range(50):
    line = prog.recvline()
    crypt = line[line.find(b':')+2:].strip()
    ans = search(crypt.decode('utf-8'))
    print(f"{ans=}")
    if ans == "":
        print(f"brak rozwiązania!: {crypt}")

    prog.sendline(bytes(ans, 'utf-8'))

#prog.interactive()