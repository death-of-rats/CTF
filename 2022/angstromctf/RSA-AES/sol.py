#!/usr/bin/env python3
import pwn
import ast
import string
from Crypto.Util.number import bytes_to_long, long_to_bytes

prog = pwn.remote('challs.actf.co', 31500)

n = 0xbb7bbd6bb62e0cbbc776f9ceb974eca6f3d30295d31caf456d9bec9b98822de3cb941d3a40a0fba531212f338e7677eb2e3ac05ff28629f248d0bc9f98950ce7e5e637c9764bb7f0b53c2532f3ce47ecbe1205172f8644f28f039cae6f127ccf1137ac88d77605782abe4560ae3473d9fb93886625a6caa7f3a5180836f460c98bbc60df911637fa3f52556fa12a376e3f5f87b5956b705e4e42a30ca38c79e7cd94c9b53a7b4344f2e9de06057da350f3cd9bd84f9af28e137e5190cbe90f046f74ce22f4cd747a1cc9812a1e057b97de39f664ab045700c40c9ce16cf1742d992c99e3537663ede6673f53fbb2f3c28679fb747ab9db9753e692ed353e3551
e = 0x10001

def send(msg: bytes):
    prog.recvuntil(b':')
    prog.sendline(msg)
    prog.recvline()
    aes = prog.recvline(keepends=False).decode('utf-8')
    aes = hex(bytes_to_long(ast.literal_eval(aes)))[2:]
    return aes


rsa = int(prog.recvline().strip())
aes = send(str(rsa).encode('utf-8'))

print(f"{     rsa=}")
print(f"{     aes=}")

flag = b'actf{'
internal = string.ascii_letters+string.digits+'_'
for c in internal:
    t_flag = flag + 11*c.encode('utf-8')

    msg = pow(bytes_to_long(t_flag), e, n)
    test_aes = send(str(msg).encode('utf-8'))
    print(f"{test_aes=}")

    if(test_aes in aes):
        print(f"{t_flag=}")
