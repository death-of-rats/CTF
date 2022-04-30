#!/usr/bin/env python3
import pwn

inputPrompt = b'\nUsername :'
arrow = b'-> '

prog = pwn.process('./aes-2.py', )

def spaced_print(msg:str, creds):
    print(msg+" "*(14-len(msg)), end="")
    [print(f"{creds[i:i+32]}", end=" ") for i in range(0, len(creds), 32)]
    print("")    

line = prog.recvline()
print(f"{line=}")
alice = line[16:16+64]
alice_cipher = line[16+64+4:16+64+4+64]
spaced_print("alice:", alice)
spaced_print("alice_cipher:", alice_cipher)

prog.recvuntil(inputPrompt)
payload = alice + alice_cipher[32:]
spaced_print("payload", payload)
prog.sendline(payload)

line = prog.recvline()
creds = line[3+line.find(arrow):].strip()
spaced_print("creds", creds)
prog.recvuntil(inputPrompt)
payload = payload + creds[-32:]
spaced_print("payload", payload)
prog.sendline(payload)


line = prog.recvline()
creds = line[3+line.find(arrow):].strip()
spaced_print("creds", creds)
prog.recvuntil(inputPrompt)
payload = payload + creds[-32:]
spaced_print("payload",payload)
prog.sendline(payload)

line = prog.recvline()
creds = line[3+line.find(arrow):].strip()
spaced_print("creds", creds)
prog.recvuntil(inputPrompt)
last_16 = int(creds[-32:],16)
last_16 = last_16 ^ int(alice[-32:],16) ^ int(alice_cipher[:32], 16)
payload = payload + bytes(hex(last_16)[2:],'utf-8')
spaced_print("payload",payload)
prog.sendline(payload)

line = prog.recvall()
creds = line[3+line.find(arrow):].strip()
spaced_print("creds", creds)

print(prog.recvall())
