# babymix

## Challenge

Find the password that will give you the flag.
file: babymix

## Solution

Using ghidra to analyze the program I extracted a set of checks that are made on the input:

```
pass[8] + pass[0xc] + pass[0xc] - pass[0x11] == 0x99
(pass[2] ^ pass[0x13]) + pass[0x15] + pass[10] == 0xd9
(pass[0x10] ^ pass[0]) + pass[3] + pass[0x10] + (pass[0x10] ^ pass[5]) == 0xe8
(pass[0] ^ pass[0x13]) + pass[10] + pass[3] + pass[3] - pass[0x13] == 0x148
pass[2] - pass[0x13] + pass[10] - pass[8] == 0x4a
pass[0x11] - pass[9] + pass[4] + pass[0xb] + pass[0x11] - pass[1] == 0xa6
pass[10] + pass[5] + pass[0x12] - pass[9] + pass[10] + pass[0xe] == 0x19d
pass[0x15] + pass[1] + pass[0xb] - pass[2] + pass[0x11] - pass[0xd] + pass[8] - pass[0xc] + pass[5] - pass[0x10] == 0x62
(pass[0xc] ^ pass[0x10]) + pass[6] - pass[0xd] + pass[0x11] - pass[0xb] + (pass[0xd] ^ pass[0x13]) == 0x55
(pass[7] ^ pass[2]) + pass[4] - pass[0x10] == 0x4d
pass[10] + pass[7] + (pass[0xe] ^ pass[8]) + pass[1] + pass[5] + pass[0xe] - pass[3] + pass[8] - pass[0x11] == 0x180 
pass[2] + pass[0x11] + pass[0xf] - pass[0x15] + pass[2] - pass[4] + pass[4] - pass[0]== 0x109 
pass[6] + pass[7] + pass[0x15] - pass[0x12] + pass[2] + pass[0xf] + pass[0x11] - pass[4] + pass[5] - pass[0x12] == 0xfa 
(pass[0x12] ^ pass[0xc]) + pass[7] - pass[0x12] + pass[0x15] - pass[0x13] + pass[0x10] - pass[0x15] == 0x4b 
pass[6] + pass[9] + (pass[2] ^ pass[10]) + pass[7] + pass[2] + pass[0xd] + pass[0x14] + (pass[0x10] ^ pass[3]) == 0x26d
pass[1] - pass[0x13] + (pass[2] ^ pass[0xe]) + pass[0] + pass[0xb] + pass[8] - pass[3] == 0x11b
pass[0xd] - pass[0x13] + *pass[0xb] ^ pass[0]) + (pass[0xe] ^ pass[0]) + pass[0x10] - pass[0xe] == 0x6a 
pass[3] - pass[0x12] + pass[0]- pass[0x14] + pass[0x13] + pass[10] + pass[10] + pass[0x13] == 0x129 
pass[0x12] + pass[0x14] + pass[0]- pass[0xf] == 0x9c 
pass[3] - pass[0x11] + pass[10] - pass[0x14] + pass[0xd] - pass[8] == 0x55 
pass[10] - pass[2] + pass[4] + pass[0x13] + (pass[0x11] ^ pass[0xc]) + pass[3] - pass[0x11] == 0xa0 
pass[0xc] - pass[10] + pass[0xb] - pass[0x15] == 0x24 
(pass[0x10] ^ pass[5]) + pass[6] - pass[0x10] + (pass[0x13] ^ pass[0x12]) == 0x66 
pass[0x15] - pass[5] + pass[6] - pass[0xd] + (pass[0xf] ^ pass[10]) == -0x30 
(pass[4] ^ pass[6]) + pass[0xc] - pass[0xb] + (pass[3] ^ pass[5]) == 0x1d
pass[0x15] - pass[0xb] + pass[8] - pass[0xf] + pass[9] - pass[2] + pass[6] - pass[0xe] == -0x6d
pass[0x11] + pass[0xb] + pass[0] + pass[0x10] + pass[0x13] - pass[7] == 0x169
(pass[0x13] ^ pass[0xf]) + pass[0xf] + pass[3] == 0x128
```

To solve this I write (copy&paste&edit) python program. Z3 solver do the job.

```python
# inspired by https://medium.com/tsscyber/ctf-writeup-you-shall-not-pass-2c7a9254549b
from z3 import *

def z3_byte_comparator(b):
       return int(str(b)[1:])

x = [BitVec('x{}'.format(i), 8) for i in range(0x16)]

s = Solver()

s.add( x[8] + x[0xc] + x[0xc] - x[0x11] == 0x99)
s.add((x[2] ^ x[0x13]) + x[0x15] + x[10] == 0xd9)
s.add((x[0x10] ^ x[0]) + x[3] + x[0x10] + (x[0x10] ^ x[5]) == 0xe8)
s.add((x[0] ^ x[0x13]) + x[10] + x[3] + x[3] - x[0x13] == 0x148)
s.add(x[2] - x[0x13] + x[10] - x[8] == 0x4a)
s.add(x[0x11] - x[9] + x[4] + x[0xb] + x[0x11] - x[1] == 0xa6)
s.add(x[10] + x[5] + x[0x12] - x[9] + x[10] + x[0xe] == 0x19d)
s.add(x[0x15] + x[1] + x[0xb] - x[2] + x[0x11] - x[0xd] + x[8] - x[0xc] + x[5] - x[0x10] == 0x62)
s.add((x[0xc] ^ x[0x10]) + x[6] - x[0xd] + x[0x11] - x[0xb] + (x[0xd] ^ x[0x13]) == 0x55)
s.add((x[7] ^ x[2]) + x[4] - x[0x10] == 0x4d)
s.add(x[10] + x[7] + (x[0xe] ^ x[8]) + x[1] + x[5] + x[0xe] - x[3] + x[8] - x[0x11] == 0x180 )
s.add(x[2] + x[0x11] + x[0xf] - x[0x15] + x[2] - x[4] + x[4] - x[0]== 0x109 )
s.add(x[6] + x[7] + x[0x15] - x[0x12] + x[2] + x[0xf] + x[0x11] - x[4] + x[5] - x[0x12] == 0xfa )
s.add((x[0x12] ^ x[0xc]) + x[7] - x[0x12] + x[0x15] - x[0x13] + x[0x10] - x[0x15] == 0x4b )
s.add(x[6] + x[9] + (x[2] ^ x[10]) + x[7] + x[2] + x[0xd] + x[0x14] + (x[0x10] ^ x[3]) == 0x26d)
s.add(x[1] - x[0x13] + (x[2] ^ x[0xe]) + x[0] + x[0xb] + x[8] - x[3] == 0x11b)
s.add(x[0xd] - x[0x13] + (x[0xb] ^ x[0]) + (x[0xe] ^ x[0]) + x[0x10] - x[0xe] == 0x6a )
s.add(x[3] - x[0x12] + x[0]- x[0x14] + x[0x13] + x[10] + x[10] + x[0x13] == 0x129 )
s.add(x[0x12] + x[0x14] + x[0]- x[0xf] == 0x9c )
s.add(x[3] - x[0x11] + x[10] - x[0x14] + x[0xd] - x[8] == 0x55 )
s.add(x[10] - x[2] + x[4] + x[0x13] + (x[0x11] ^ x[0xc]) + x[3] - x[0x11] == 0xa0 )
s.add(x[0xc] - x[10] + x[0xb] - x[0x15] == 0x24 )
s.add((x[0x10] ^ x[5]) + x[6] - x[0x10] + (x[0x13] ^ x[0x12]) == 0x66 )
s.add(x[0x15] - x[5] + x[6] - x[0xd] + (x[0xf] ^ x[10]) == -0x30 )
s.add((x[4] ^ x[6]) + x[0xc] - x[0xb] + (x[3] ^ x[5]) == 0x1d)
s.add(x[0x15] - x[0xb] + x[8] - x[0xf] + x[9] - x[2] + x[6] - x[0xe] == -0x6d)
s.add(x[0x11] + x[0xb] + x[0] + x[0x10] + x[0x13] - x[7] == 0x169)
s.add((x[0x13] ^ x[0xf]) + x[0xf] + x[3] == 0x128)

if s.check() == sat:
    model = s.model()
    result = sorted([byte for byte in model], key = z3_byte_comparator)
    ch = [chr(int(str(model[b]))) for b in result]
    print(''.join(ch))

```
