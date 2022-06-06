

# This file was *autogenerated* from the file sol.sage
from sage.all_cmdline import *   # import sage library

_sage_const_35 = Integer(35); _sage_const_98 = Integer(98); _sage_const_434252269029337012720086440207 = Integer(434252269029337012720086440207); _sage_const_16378704336066569231287640165 = Integer(16378704336066569231287640165); _sage_const_377857010369614774097663166640 = Integer(377857010369614774097663166640); _sage_const_434252269029337012720086440208 = Integer(434252269029337012720086440208); _sage_const_2 = Integer(2); _sage_const_4 = Integer(4); _sage_const_3 = Integer(3); _sage_const_73 = Integer(73); _sage_const_88591 = Integer(88591); _sage_const_3882601 = Integer(3882601); _sage_const_360301137196997 = Integer(360301137196997); _sage_const_0x3bfac870bfc0f906bd2cc5ea5 = Integer(0x3bfac870bfc0f906bd2cc5ea5); _sage_const_0x53b5c858be1b02db42602c5d2 = Integer(0x53b5c858be1b02db42602c5d2); _sage_const_0x3016bf3f2ea21fbd8f7f5413a = Integer(0x3016bf3f2ea21fbd8f7f5413a); _sage_const_0x30048bdf6c7e3bc7ba1f6a687 = Integer(0x30048bdf6c7e3bc7ba1f6a687); _sage_const_0 = Integer(0)
a = -_sage_const_35 
b = _sage_const_98 
p = _sage_const_434252269029337012720086440207 
Gx = _sage_const_16378704336066569231287640165 
Gy = _sage_const_377857010369614774097663166640 
ec_order = _sage_const_434252269029337012720086440208 
order_factor = _sage_const_2 **_sage_const_4  * _sage_const_3  * _sage_const_73  * _sage_const_88591  * _sage_const_3882601  * _sage_const_360301137196997 

departed_x = _sage_const_0x3bfac870bfc0f906bd2cc5ea5 
departed_y = _sage_const_0x53b5c858be1b02db42602c5d2 
present_x = _sage_const_0x3016bf3f2ea21fbd8f7f5413a 
present_y = _sage_const_0x30048bdf6c7e3bc7ba1f6a687 

E = EllipticCurve(Integers(p),[_sage_const_0 ,_sage_const_0 ,_sage_const_0 ,a,b])
G = E(Gx,Gy)
Q = E(departed_x,departed_y)

k = _sage_const_2 
Fy = GF(p**k, 'y')
Ee = EllipticCurve(Fy,[a,b])


Qe = Ee(Q)
Ge = Ee(G)
R = Ee.random_point()
m = R.order()

d = gcd(m, Q.order())
print(f"{d=}")
RR = (m//d)*R

assert Q.order()/RR.order() in ZZ
assert Q.order() == RR.order()

n = G.order()

al = Ge.weil_pairing(RR,n)
be = Qe.weil_pairing(RR,n)
dd = be.log(al)

print(dd)
