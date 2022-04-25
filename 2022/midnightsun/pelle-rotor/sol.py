#!/usr/bin/env python
import pwn
from gmpy2 import gcd, next_prime
from itertools import combinations
from Crypto.Util.number import long_to_bytes

DIGIT_MODULE_SEARCH_MAX = 100000

prog = pwn.process('./pelles_rotor_supported_arithmetic.py')

def cleanUpN(n:int):
    prime = 1
    for _ in range(100):
        prime = next_prime(prime)
        while n % prime == 0:
            n = n // prime
    return n

def send(c,i):
    global prog
    prog.sendline(b'1')
    prog.recvline()
    prog.sendline(bytes(str(c),'utf-8'))
    prog.recvline()
    prog.sendline(bytes(str(i),'utf-8'))
    cipher = prog.recvline().strip()

    if b'Come on' not in cipher:
        return int(cipher)
    return -1

flag_power = 3331646268016923629
e = 65537
flag_cipher = int(prog.recvline().strip()[15:])
print(f"C={flag_cipher}\n")

prog.recvlines(4)

sets=[[10,12,120]
     ,[2,3,6]
      ,[123,432,123*432]]

gcdSet= []
for set in sets:
    v = [send(vi, 0) for vi in set]
    d = v[0]*v[1]-v[2]
    if d == 0:
        print(f"kiepski dobór parametrów: {set}")
        continue
    gcdSet.append(d)

if len(gcdSet) < 2:
    print(f"nie wyliczę N....")
    exit(1)

subsets = combinations(gcdSet, 2)

ns = [cleanUpN(gcd(s1,s2)) for s1,s2 in subsets]
np = ns[0]
if all(el == np for el in ns):
    print(f"N={np}\n\nmax_len = {len(str(np))}\n")
else:
    print(f"N-ki się nie zgadzają... {ns}")

N = np
maxSize = len(str(N))
d_numbers = []
msg = 2
cs = []
for i in range(maxSize+1):
    cs.append(send(msg,i))
dSize = 0
for i,c in enumerate(cs):
    if c == cs[0] and i > 0:
        dSize = i
        break
if dSize == 0:
    print(f"nie znaleziono rozmiaru d")
    exit(1)
print(f"dSize = {dSize}\n")

d_exp = 10**(dSize-1)

for ind in range(dSize):
    cp = cs[ind]
    cn = cs[ind+1]
    for digit in range(10):
        m_10il = pow(msg,digit*d_exp*10,N)
        m_i = msg**digit

        for _ in range(DIGIT_MODULE_SEARCH_MAX):
            if cn % m_i == 0:
                break
            cn += N
        if cn % m_i != 0:
            print(".", end="")
            break

        m_10d = cn // m_i
        cp_10 = (m_10il * m_10d) % N
        if cp_10 == pow(cp, 10, N):
            num = digit
            d_numbers.append(digit)
            break
if len(d_numbers) != dSize:
    print(f"d not found, only {len(d_numbers)} digits of {dSize}!!!")
    print(d_numbers)
    exit(1)

d = int("".join([str(vv) for vv in d_numbers]))
print(f"d={d}\ntest= 13=={pow(pow(13,e,N),d,N)}\n")

fi = e*d-1
D = pow(flag_power, -1, fi)
M = pow(flag_cipher, D, N)
print(f"{long_to_bytes(M)}")
