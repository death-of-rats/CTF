from Crypto.Util.number import getStrongPrime, getPrime, isPrime, bytes_to_long

FLAG = b"Securinets{REDACTED_REDACTED}"

def genPrime(prime):
    while True:
        a = getPrime(256)
        p = 2*prime*a + 1
        if isPrime(p):
            break
    while True:
        b = getPrime(256)
        q = 2*prime*b + 1
        if isPrime(q):
            break
    return p, q

prime = getStrongPrime(512)
p1, q1 = genPrime(prime)
p2, q2 = genPrime(prime)
assert p1 != p2 != q1 != q2

n1 = p1*q1
n2 = p2*q2
e = 65537

print(f"prime: {prime}")
print(f"fi1: {(p1-1)*(q1-1)}")
print(f"fi2: {(p2-1)*(q2-1)}")

m1 = bytes_to_long(FLAG[:len(FLAG)//2])
m2 = bytes_to_long(FLAG[len(FLAG)//2:])

c1 = pow(m1, e, n1)
c2 = pow(m2, e, n2)

print(f"n1 = {n1}")
print(f"n2 = {n2}")
print(f"e = {e}")
print(f"c1 = {c1}")
print(f"c2 = {c2}")