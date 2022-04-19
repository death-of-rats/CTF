#!/usr/bin/env python
from cmath import nan
from os import remove
import pwn
from gmpy import next_prime
    
prog = pwn.process('./pelles_rotor_supported_arithmetic.py')

def send(c):
    global prog
    prog.sendline('1')
    prog.recvline()
    prog.sendline(c)
    prog.recvline()
    prog.sendline('0')
    cipher = prog.recvline().strip()

    if b'Come on' not in cipher:
        #print(cipher)
        return int(cipher)
    return -1

c = 5
cipher = 1
flag_power = 3331646268016923629
e = 65537
ciphers = []
flag_cipher = int(prog.recvline().strip()[15:])
print(flag_cipher)

prog.recvlines(4)

c2 = send('2')
c3 = send('3')
c6 = send('6')

nn = c2*c3-c6
n = nn
for i in range(10000):
    if nn % (2+i) == 0:
        n = nn // (2+i)

print(f"n: {n}")

print(send(str(pow(flag_cipher, flag_power, n))))

while cipher > 0:
    cipher = send(str(c))
   
    if cipher > 0:
        ciphers.append({
            'pt': c,
            'ct': cipher
        })
        c = next_prime(c)
