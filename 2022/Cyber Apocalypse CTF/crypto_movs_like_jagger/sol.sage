
a = -35
b = 98
p = 434252269029337012720086440207
Gx = 16378704336066569231287640165
Gy = 377857010369614774097663166640
ec_order = 434252269029337012720086440208
order_factor = 2**4 * 3 * 73 * 88591 * 3882601 * 360301137196997

departed_x = 0x3bfac870bfc0f906bd2cc5ea5
departed_y = 0x53b5c858be1b02db42602c5d2
present_x = 0x3016bf3f2ea21fbd8f7f5413a
present_y = 0x30048bdf6c7e3bc7ba1f6a687

E = EllipticCurve(Integers(p),[0,0,0,a,b])
G = E(Gx,Gy)
Q = E(departed_x,departed_y)

k = 2
Fy = GF(p^k, 'y')
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
