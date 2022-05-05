
maxUint64 = (1 << 64) - 1

multiplier = 47026247687942121848144207491837523525
mulHigh    = multiplier >> 64
mulLow     = multiplier & maxUint64

increment = 117397592171526113268558934119004209487
incHigh   = increment >> 64
incLow    = increment & maxUint64

initializer = 245720598905631564143578724636268694099
initHigh    = initializer >> 64
initLow     = initializer & maxUint64

L = 3
H = 3

def rotR(X:int, rotBy:int):
    r = X >> rotBy
    r |= (X & (maxUint64^ (maxUint64 << rotBy))) << (64-rotBy)
    return r

def add():
    global L, H
    L = L + incLow
    c = L>>64
    L = L & maxUint64
    H = (H + incHigh + c) & maxUint64

def mul():
    global L, H
    m = L * mulLow
    hi = m>>64
    lo = m & maxUint64
    hi += H * mulLow
    hi += L * mulHigh
    L = lo
    H = hi & maxUint64

def next_u64():
    global L, H
    mul()
    add()
    rotBy = H>>58
    X = H^L
    return rotR(X, rotBy)

def findRotVal(r:int) -> int:
    R = bytes(bin(r)[2:], 'utf-8')
    R = b'0'*(64-len(R))+R
    return 6
  #  for i in range(64):

print(f"{incHigh=}, {incHigh.bit_length()}")
print(f"{incLow=}, {incLow.bit_length()}")
print(f"{mulHigh=}, {mulHigh.bit_length()}")
print(f"{mulLow=}, {mulLow.bit_length()}")
