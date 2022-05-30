import pwn
from hashlib import sha256
import binascii

p = pwn.remote('134.209.178.167', 31243)
BLOCK_SIZE = 32

print(p.recvuntil(b'responses.'))

def decrypt_block(block, secret):
    enc_block = b''
    for i in range(BLOCK_SIZE):
        val = (block[i]-secret[i]) % 256
        enc_block += bytes([val])
    return enc_block

def decode(cmd: bytes, msg: bytes):
    output_prefix = b'Command executed: ' + cmd + b'\n'
    if len(output_prefix) < 32:
        print("Cann't do!")
        return b''
    
    h = sha256(msg[:32] + output_prefix[:32]).digest()
    blocks = [msg[i:i+BLOCK_SIZE] for i in range(0, len(msg), BLOCK_SIZE)]
    ct = b''
    for block in blocks[1:]:
        dec_block = decrypt_block(block, h)
        h = sha256(block + dec_block).digest()
        ct += dec_block
    
    return ct


def send_cmd(cmd: bytes) -> bytes:
    p.recvuntil(b'>')
    p.sendline(cmd)
    enc_cmd = binascii.unhexlify(p.recvline().strip())
    #print(f"{enc_cmd=}\t{len(enc_cmd)=}\n")
    return enc_cmd


o = send_cmd(b'cat secret.txt')
print(decode(b'cat secret.txt', o))

