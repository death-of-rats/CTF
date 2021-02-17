# plagiarism

I didn't solve this challenge. After CTF I read the writeup and mentioned in it article and implement GDC in python with SageMath.

## Challenge

Can I copy your CTF challenge?

Yeah, just change it up a bit so it doesn't look obvious you copied.

https://hxp.io/blog/1/RuCTF%20Quals%202014:%20Crypto%20500%20%22decrypt%20message%22%20writeup/

>Two agents, Blex and Kane, have simultaneously known very secret message and transmitted it to Center. You know following:
>1) They used RSA with this public key
>2) They sent exactly the same messages except the signatures (name appended, eg. "[message]Blex")
>3) They did encryption this way:
>
>m = int(message.encode("hex"), 16)
>c = pow(m, e, N)
>
>4) And here are cryptograms you have intercepted:
>
>N = 25898966400928827905718377946331123070958718286581765316565582158865227877882475404853218079499084099440419144196215764927720893687968939899067275095801562867742359933997487928281899714724738097735994026225339488710478292473051567851786254924548138570069406420407124627567648479424564834446192417334669768477661434992797176428220265984651288944265998446714590797833756720922745187467388408600309665467669255896919554072379878017822219455974525233467767926938557154083882126002952139561283708342676308894318951822068027821029295524097544028901807902120777407151278396388621981625398417573347316888458337381776303199529
>
>e = 1048577
>
>ciphertext_Blex = 11140520553087800834883326476247582685177207584737264356946559762068509060522907835540767944557089926814767920501376431871780404000550271362410228709616559148950928004959648199391157781102695421411667843970881959939688515679415870087007797819271601359811630724878746762862603629420061133824605384527474682526549557804674160851967543475275374840169790764048711047622418045734436512050742433282306694490346907876574514077395835974083376649624559301087384766644865104383786285302561584731767419571603248493060257358632833957327996996960955767927114473513709882904104552609194519132931270741118197821776138632855021619178
>
>ciphertext_Kane = 2922817623733019475805146570530296261205732600738503605503192845278422660686627490817081424885152809772315629265930072636690234953045955503581182067349322827011065359648958225896393305011175960879100475146203207801533980643261035226402857047007061320653920746872424363923515091038846823007819033456503365649022294092944985887626605207259444051959239244136999684366533551627508385114998024232490369665950339127904350803268889205463047713233591604324960184727360413931125906144631968128488876241314939855024305076160092193380013725939761970042406866169417457376487954247442308318888399299295082898238584625937490546472
>
>Now tell me that secret message! (The answer for this task starts from 'dice{') 

## Solution

So we have two ciphertexts:

C<sub>1</sub> = P<sub>1</sub><sup>e</sup> mod(N)

C<sub>2</sub> = P<sub>2</sub><sup>e</sup> mod(N)

where second text is simply first with known difference:

P<sub>2</sub> = P<sub>1</sub>+&delta;

so we have after substitution:

f = P<sub>1</sub><sup>e</sup> mod(N) - C<sub>1</sub>

g = (P<sub>1</sub>+&delta;)<sup>e</sup> mod(N) - C<sub>2</sub>

Calculating **GCD(f,g)** will give us common dividor **a \* P<sub>1</sub> + b** so **P<sub>1</sub> = <sup>-b</sup>&frasl;<sub>a</sub>**.

```python

def franklin(n, e, delta, c1, c2):
    R = PolynomialRing(Zmod(n), 'X')
    X = R.gen()
    f1 = (X)**e - c1
    f2 = (X + delta)**e - c2
    r = gcd(f1, f2)
    co = r.coefficients()
    return -co[0]//co[1]

```

The 'problem' was calculating GCD in a reasonable time. The attached [article](polydivide.pdf) describes the algorithm with time approximation **O(n lg<sup>2</sup>n)**. Its implementation in python with SageMath is:

```python

def gcd(a0,a1):
    while True:
        print(a0.degree(), end=", ", flush=True)
        if a0 % a1 == 0:
            return a1
        if a0.degree() == a1.degree():
            a1 = a0%a1
        R = hgcd(a0,a1)
        [b0,b1] = R.dot(np.array([a0,a1]).transpose()).transpose()
        if b0%b1==0:
            return b1
        c = b0 % b1
        a0 = b1
        a1 = c


def hgcd(a0,a1):
    if a1.degree() <= (a0.degree()//2):
        return np.array([[1,0],[0,1]])

    m = a0.degree()//2
    X = a0.variables()[0]
    b0 = a0 // X**m
    b1 = a1 // X**m
    
    R = hgcd(b0,b1)
    [d,e] = (R.dot(np.array([a0,a1]).transpose())).transpose()
    ff = d % e
    m = m // 2
    g0 = e // X**m
    g1 = ff // X**m

    S = hgcd(g0,g1)
    q = d // e
    return S.dot(np.array([[0,1],[1,-q]])).dot(R)

```

The complete implementation is in the [sol.py](sol.py) file.