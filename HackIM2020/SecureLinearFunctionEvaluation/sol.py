#!/usr/bin/env python3

from pwn import *
from Crypto.Util.number import *
from hashlib import sha256
import json

p = 0xffffffffffffffffc90fdaa22168c234c4c6628b80dc1cd129024e088a67cc74020bbea63b139b22514a08798e3404ddef9519b3cd3a431b302b0a6df25f14374fe1356d6d51c245e485b576625e7ec6f44c42e9a637ed6b0bff5cb6f406b7edee386bfb5a899fa5ae9f24117c4b1fe649286651ece45b3dc2007cb8a163bf0598da48361c55d39a69163fa8fd24cf5f83655d23dca3ad961c62f356208552bb9ed529077096966d670c354e4abc9804f1746c08ca237327ffffffffffffffff
size = 128

def split(num):
    for i in range(num-2):
        dv = i+2
        if num % i == 0:
            return i
    return None


# nc crypto2.ctf.nullcon.net 5000
conn = remote('crypto2.ctf.nullcon.net', 5000)
conn.recvline()
cs = json.loads(conn.readline())

print(f"I get cs[{len(cs)}]")

inp = " ".join([f'({c},{c},{1})' for c in cs])
conn.sendline(inp)

conn.recvuntil('Server response:\n')
ret = conn.recvline()
#print(ret[:32], flush=True)
#print(ret[-32:], flush=True)
ret = ret[1:-2]
d = ret.split(b')), ((')
#print(f'to parse {len(d)} elements')
#((3,4),(5,6))
data = []
for part in d:
    c0c1 = part.split(b'), (')
    gy0 = c0c1[0].strip().split(b',')
    gy1 = c0c1[1].strip().split(b',')
    item = ((
             int(gy0[0].strip().replace(b'(',b'').replace(b')',b'')), 
             int(gy0[1].strip().replace(b'(',b'').replace(b')',b''))
            ),
            (
             int(gy1[0].strip().replace(b'(',b'').replace(b')',b'')), 
             int(gy1[1].strip().replace(b'(',b'').replace(b')',b''))
            ))
    data.append(item)

b = []
a = []
one_hash = int(sha256(long_to_bytes(1)).hexdigest(), 16)
for i in range(len(data)):
    c0, c1 = data[i]
    g_powered, y0_hash = c0
    g_hash = int(sha256(long_to_bytes(g_powered)).hexdigest(), 16)
    bi = g_hash ^ y0_hash
    b.append( bi )
    _, y1_hash = c1
    a.append( one_hash ^ y1_hash ^ bi )

print(a)
print(b)

conn.recvuntil('Enter a:')
conn.sendline(str(a))
conn.recvuntil('Enter b:')
conn.sendline(str(b))

print(conn.recvall(), flush=True)
conn.close()

# hackim20{this_was_the_most_fun_way_to_include_curveball_that_i_could_find}