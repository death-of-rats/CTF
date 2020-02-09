#!/usr/bin/env python3

import json
from pwn import *
from Crypto.Util.number import *

sbox = [221, 229, 120, 8, 119, 143, 33, 79, 22, 93, 239, 118, 130, 12, 63, 207, 90, 240, 199, 20, 181, 4, 139, 98, 78, 32, 94, 108, 100, 223, 1, 173, 220, 238, 217, 152, 62, 121, 117, 132, 2, 55, 125, 6, 34, 201, 254, 0, 228, 48, 250, 193, 147, 248, 89, 127, 174, 210, 57, 38, 216, 225, 43, 15, 142, 66, 70, 177, 237, 169, 67, 192, 30, 236, 131, 158, 136, 159, 9, 148, 103, 179, 141, 11, 46, 234, 36, 18, 191, 52, 231, 23, 88, 145, 101, 17, 74, 44, 122, 75, 235, 175, 54, 40, 27, 109, 73, 202, 129, 215, 83, 186, 7, 163, 29, 115, 243, 13, 105, 184, 68, 124, 189, 39, 140, 138, 165, 219, 161, 150, 59, 233, 208, 226, 176, 144, 113, 146, 19, 224, 111, 126, 222, 178, 47, 252, 99, 87, 134, 249, 69, 198, 164, 203, 194, 170, 26, 137, 204, 157, 180, 168, 162, 56, 81, 253, 213, 45, 21, 58, 24, 171, 37, 82, 53, 50, 84, 196, 232, 242, 244, 64, 80, 10, 114, 212, 187, 205, 28, 51, 182, 16, 107, 245, 211, 85, 92, 195, 5, 197, 200, 31, 183, 61, 123, 86, 167, 154, 41, 151, 35, 247, 246, 153, 95, 206, 149, 76, 112, 71, 230, 106, 188, 172, 241, 72, 156, 49, 14, 214, 155, 110, 102, 116, 128, 160, 135, 104, 77, 91, 190, 60, 42, 185, 96, 97, 251, 218, 133, 209, 65, 227, 3, 166, 255, 25]
p = [5, 9, 1, 8, 3, 11, 0, 12, 7, 4, 14, 13, 10, 15, 6, 2]

q = [6, 2, 15, 4, 9, 0, 14, 8, 3, 1, 12, 5, 7, 11, 10, 13]
qbox = bytearray(len(sbox))
for i in range(len(sbox)):
    qbox[sbox[i]] = i

def repeated_xor(p, k):
    return bytearray([p[i] ^ k[i % len(k)] for i in range(len(p))])

def revert(hash: str, proposal_key: bytes):
    value = int(hash, 16)
    state = long_to_bytes(value)
    for _ in range(16):
        tmp = bytearray(16)
        for i in range(len(state)):
            tmp[q[i]] = state[i]
        state = tmp
        for i in range(len(state)):
            state[i] = qbox[state[i]]
        state = repeated_xor(state, proposal_key)
    return (chr(proposal_key[0]), bytes_to_long(state))
    
def sol(hashes):
    res = []
    for h in hashes:
        rkey = [b'p' + b'\x0f' * 15, 
                b'r' + b'\x0f' * 15, 
                b's' + b'\x0f' * 15]
        calc = [revert(h, key) for key in rkey]
        res.append(calc)

    for i1 in range(3):
        for i2 in range(3):
            for i3 in range(3):
                if res[0][i1][1] == res[1][i2][1] and res[1][i2][1] == res[2][i3][1]: 
                    return res[0][i1][0]
    return None

def parse_hashes(line):
    coma = line.find(b':')
    ops = line[coma+2:].split(b' ')
    return [o.strip() for o in ops]

def get_winner(move):
    if move == 'p':
        return 's'
    if move == 's':
        return 'r'
    if move == 'r':
        return 'p'
    return 'p'

conn = remote('crypto1.ctf.nullcon.net', 5000)
conn.recvline()
for _ in range(20):
    data = conn.recvline()
    hashe = parse_hashes(data)
    print(hashe)
    option = get_winner(sol(hashe))
    print('Move '+option)
    conn.recvuntil('Your move:')
    conn.sendline(option)
    msg = conn.recvline()
    print(msg)

print(conn.recvall())

conn.close()

# hackim20{b4d_pr1mitiv3_beats_all!1!_7f65}