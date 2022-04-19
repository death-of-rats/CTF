import hashlib
import string

CONSTHASH = "667a32132baf411ebf34c81a242d9ef4bf72e288"


def XOR(x, y):
    return "".join([str(hex(int(a, 16)^int(b, 16)))[2:] for a,b in zip(x, y)])

commands = [32*c for c in string.printable]
hh = [hashlib.sha1(x.encode()).hexdigest() for x in commands]
[print(hhi) for hhi in hh]
h = hh[0]
for i in range(1, len(hh)):
    h = XOR(h, hh[i])

print(h)