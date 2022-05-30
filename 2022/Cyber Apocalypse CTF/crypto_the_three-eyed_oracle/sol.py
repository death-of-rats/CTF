from tkinter import W
import pwn
import binascii
import string
from Crypto.Util.number import long_to_bytes

prefix_len = 12

def send(msg: bytes):
    p.recvuntil(b'>')
    p.sendline(msg)
    enc = p.recvline().strip()
    return binascii.unhexlify(enc)

p = pwn.remote('157.245.47.33',31872)

flag = b'HTB{'
for i in range(1,32):
    padding = b'A'*(32-i)
    base = send(binascii.hexlify(padding))
    for ch in [bytes(c, encoding='utf-8') for c in string.printable]:
        m = padding + flag + bytes(ch)
        test = send(binascii.hexlify(m))
        if test[32:48] == base[32:48]:
            flag += ch
            print(flag)
            if ch == b'}':
                exit(0)
            break