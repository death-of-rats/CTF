# SecureLinearFunctionEvaluation

## Challenge

> In this challenge we provide a sytem that calculates a * x + c in F_2^128 , where a and b are server supplied and x is client supplied. 
> To get the flag you have to find a and b. Server runs at: 
>
> ```nc crypto2.ctf.nullcon.net 5000```
>
> file: [lfe.py](lfe.py)

### Solution

Let us analyze the server code. Two 128bit numbers *a*, *b* are generated. Then we get 128 ```cs``` random values that constrain our input *(g, y0, y1)*:

```math
(y0 * y1) % p == cs
```

Ok, so what happens to out input? For every set, the program gets random 2 numbers r0, r1 (mod p). Calculate and return to us *(c0, c1)*:
```math
m0 = b[i]
m1 = (a[i] + b[i]) % 2
c0 = (
    pow(g, r0, p), 
    int(sha256(long_to_bytes(pow(y0, r0, p))).hexdigest(), 16) ^ m0
    )
c1 = (
    pow(g, r1, p), 
    int(sha256(long_to_bytes(pow(y1, r1, p))).hexdigest(), 16) ^ m1
    )
```

So *m0* is just a bit from the *b* value. *m1* on the other hand is simply *xor* of *a* and *b*, then: ```a[i] = m1 ^ m0```.

To get b[i] I should know last bit of ```int(sha256(long_to_bytes(pow(y0, r0, p))).hexdigest(), 16)```. And I will know this if ```g == y0```, I will get ```pow(g, r0, p)``` from the server answer and sha256 it, convert to hex and compare with second item in the c0 pair to get *m0*. Ok, we have *b*. What with *a*? The trick with ```g == y0```, cannot be used second time, because of the assert: ```(y0 * y1) % p == cs```. How to know in advance the result of ```pow(y1, r1, p)```? Use ```y1 = 1```, it will always gice you *1*. So, what about assertion? If ```y1 == 1```, then *y0* should be *cs*, and *g* also *cs*.

```python
...
inp = " ".join([f'({c},{c},{1})' for c in cs])
conn.sendline(inp)
...
```

When we get the result from the server we can do the math: 

```python
...
b = []
a = []
one_hash = int(sha256(long_to_bytes(1)).hexdigest(), 16)
for i in range(len(data)):
    c0, c1 = data[i]
    g_powered, y0_hash = c0
    g_hash = int(sha256(long_to_bytes(g_powered)).hexdigest(), 16)
    bi = g_hash ^ y0_hash
    b.append( bi )
    _, y1_hash = c1
    a.append( one_hash ^ y1_hash ^ bi )

print(a)
print(b)
```