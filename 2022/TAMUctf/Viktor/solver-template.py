from pwn import *
import hashlib

CONSTHASH = "667a32132baf411ebf34c81a242d9ef4bf72e288"


def XOR(x, y):
    return "".join([str(hex(int(a, 16)^int(b, 16)))[2:] for a,b in zip(x, y)])


  #  hashList = [hashlib.sha1(x.encode()).hexdigest() for x in inputList]

p = remote("tamuctf.com", 443, ssl=True, sni="viktor")
p.interactive()
