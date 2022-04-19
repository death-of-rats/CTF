#!/usr/bin/env python

import math
from Crypto.Util.number import long_to_bytes

p = 320907854534300658334827579113595683489
g = 3
    #A = pow(g,a,p) #236498462734017891143727364481546318401
A = 236498462734017891143727364481546318401

for i in range(1000000000000000):
    A1 = A+i*p
    v = math.log(A1, 3)
    if v.is_integer():
        AA = pow(g, int(v), p)
        if(AA == A):
            print(v)
            print(long_to_bytes(v))