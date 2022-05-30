#!/usr/bin/env python3
#
import pwn
import ast
import string
from Crypto.Util.number import bytes_to_long, long_to_bytes
from sympy import nextprime

#prog = pwn.remote('challs.actf.co', 31500)
prog = pwn.process('./rsaaes.py')
n=23100028007870325783185834854225420810294934833542002516071573559725954624158254241681531108254811992152391330196659130138562293154330788367194811021643366683965159626531673375163335903802878418922588761148831560375220232790576797320885239420328061465883494343484169205143945161452020074030236272423633651542587783663231883652666578166091932882621607201276775089510876377814861854076054384741632988719559243513691909274012936697373832908759138215954796841768884521430353724961486282715856244282784138169211412655478210437529819247752450082552313348995988653427767077759405830302351589964380906097867393519224077222417
d=6939842401192591121734987906752587245890061674132299121701225442382842067764039668652328699672383437043020475460305195741308771990106640404072487819172928981195203135431620566757570847154658791067135360456831173111795034307546371705310122204965732368002504236215569944917819495610553172064350244407722705726779950842939416856688350900937391297793156361970425401834222208765308134550815138084431002958641575681048362621060848707903209002223186224150428170316897580755806313761372979684359108114747048822425236542115249545967974464243439666000827897452100022638567865824970888498575221273968847274554834303990380428245
#n = 0xbb7bbd6bb62e0cbbc776f9ceb974eca6f3d30295d31caf456d9bec9b98822de3cb941d3a40a0fba531212f338e7677eb2e3ac05ff28629f248d0bc9f98950ce7e5e637c9764bb7f0b53c2532f3ce47ecbe1205172f8644f28f039cae6f127ccf1137ac88d77605782abe4560ae3473d9fb93886625a6caa7f3a5180836f460c98bbc60df911637fa3f52556fa12a376e3f5f87b5956b705e4e42a30ca38c79e7cd94c9b53a7b4344f2e9de06057da350f3cd9bd84f9af28e137e5190cbe90f046f74ce22f4cd747a1cc9812a1e057b97de39f664ab045700c40c9ce16cf1742d992c99e3537663ede6673f53fbb2f3c28679fb747ab9db9753e692ed353e3551
e = 0x10001

MAX_SIZE = 256

def send(msg: int):
    global e, n
    prog.recvuntil(b':')
    prog.sendline(str(msg).encode('utf-8'))
    res = prog.recvline()
    if b"bad input, exiting" in res:
        return 16*b'\x00'
    aes = prog.recvline(keepends=False).decode('utf-8')
    aes = ast.literal_eval(aes)
    return aes

def zero_iv():
    crA = send(pow(bytes_to_long(b'A'),e,n))
    send(pow(bytes_to_long(crA),e,n))

def calc_size(val: int):
    size = len(send(val))*8
    print(f"{size=}")
    # calculate size of the flag
    for i in range(17*8):
        extendedRsa = val*pow(2**i, e, n) % n
        e_aes = send(extendedRsa)
        if len(e_aes)*8 > size:
            print(f"{i+7} bits less\n\n")
            return size - (i+7 if i>0 else 16*8)

    return size
#

rsa = int(prog.recvline().strip())
aes = send(rsa)
n_bit_size = len(bin(n)[2:])

print(f"  n_len  ={n_bit_size}")
print(f"{     rsa=}")
print(f"{     aes=}")
print(f"len = {len(aes)}")

flag = b'actf{'
flag_bit_size = calc_size(rsa)

ke = n_bit_size - flag_bit_size
print(f"{ke=}")
ka = 2**(ke-2)
kb = ((2**ke)+ka)//2

flag_low_b = 0
flag_up_b = n

while True:
    k = (ka + kb)//2

    kflag = (rsa * pow(k,e,n))%n
    r_bit_size = calc_size(kflag)
    if r_bit_size >= n_bit_size:
        kb = k
    else:
        ka = k
    r_bit_size = min(r_bit_size, n_bit_size)

    low_b = 2**(r_bit_size-1) // k
    up_b = 2**r_bit_size // k

    flag_low_b = max(flag_low_b, low_b)
    flag_up_b = max(flag_up_b, up_b)

    print(f"{r_bit_size=}")
    print(f"k >= {ka}")
    print(f"k <= {kb}")
    print(f"{long_to_bytes(flag_low_b)}")
    print(f"{long_to_bytes(flag_up_b)}")

    if kb - ka <= 1:
        print("the end")
        break

#internal = string.ascii_letters+string.digits+'_'
#for c in internal:
    #t_flag = flag + c.encode('utf-8')
#
    #msg = pow(bytes_to_long(t_flag), e, n)
    #test_aes = send(str(msg).encode('utf-8'))
    #print(f"{test_aes=}")

    #if(test_aes in aes):
        #print(f"{t_flag=}")
