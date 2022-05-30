from z3 import BitVec, BitVecVal, Solver
from pwn import *
from json import loads, dumps

KEY_LEN = 27
Key = [BitVec('k', 8) for _ in range(KEY_LEN)]
IV = b"".join([bytes([i]) for i in range(255-KEY_LEN,0,-1)])
iv = [BitVecVal(c,8) for c in IV]

keyVec = iv+Key

def key_schedule(k):
    keylength = len(k)
    S = []
    for i in range(256):
        S.append(BitVecVal(i,8))
    j = BitVecVal(0, 8)
    for i in range(255):
        j = (j + S[i] + k[i%keylength]) % 256
        tmp = S[i]
        S[i] = S[j]
        S[j] = tmp
    return S

def ps_random(S, pt):
    i,j = 0,0
    ct = []
    for ch in pt:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        tmp = S[i]
        S[i] = S[j]
        S[j] = tmp
        K = S[(S[i]+S[j]) % 256]
        ct.append(K ^ ch)
    return ct

M = b'\xff'*256
S = key_schedule(keyVec)
C = ps_random(S, b'\xff'*256)


#p = remote('',444)

data = {
    'option':'encrypt',
    'iv': IV,
    'pt': M
}

print(dumps(data))







#s = Solver()
