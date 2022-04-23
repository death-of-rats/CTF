# Escrime

## Challenge

We have 2 files: [escrime.py](escrime.py) and [out.txt](out.txt). The flag was split in half and each part was encrypted with different RSA key.

## Solution

> I didn't solve this challenge during the CTF.

Analyzing the given code, one can find that both RSA keys share a common prime512. And that primes have been chosen in this form:

$$ n_i = (2\ prime512\ p_i + 1)(2\ prime512\ q_i + 1) $$

After simple transformations one has:

$$ n_i - 1 = 2\ prime512\ (2\ prime512\ p_i\ q_i + p_i+q_i) $$

So both n have prime512 as a common dividor. We can calculate it by geting 512-bit prime factor of `gcd`:

```python3
dividors = factor( gcd(n1-1,n2-1))
prime512 = next(filter(lambda v, p: len(bin(v)[2:]) == 512))
```

Going further:

$$ \frac{n_i - 1}{2\ prime512}\ = 2\ prime512\ p_i\ q_i + p_i+q_i $$

$p_i+q_i$ as sum of primes is an even number, so we can divide it by 2

$$ \frac{n_i - 1}{4\ prime512} = prime512\ p_i\ q_i + \frac{p_i+q_i}2 $$

Now we should count bits. Known value (left side) has 1023 bits, prime512 has 512 bits. $p_i$ and $q_i$ should have 256 bits, sum will have 257, division by 2 gives us 256 bits again. So $(pi+qi)/2$ is a lot smaller than prime512. It can be skiped as the rest of division by prime512. We are here for integral values, after all:

$$ ls_i = \frac{n_i-1}{4\ prime512} $$ 
$$ p_i\ q_i = ls_i\ //\ prime512 $$

Do we have to calculate further? To decrypt the flag, we need to find di. To find di, we need to have fii. And what is fii?

$$ ni = (2 prime512 pi + 1)(2 prime512 qi + 1) $$
$$ fii = 2 prime512 pi * 2 prime512q1 = 4 prime512^2 pi qi $$

And $ p_i\ q_i $ we already have.

[Solution code](sol.py)