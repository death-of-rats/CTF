# Escrime

## Challenge

We have 2 files: [escrime.py](escrime.py) and [out.txt](out.txt). The flag was split in half and each part was encrypted with different RSA key.

## Solution

> I didn't solve this challenge during the CTF.

Analyzing the given code, one can find that both RSA keys share a common prime512. And that primes have been chosen in this form:

<img src="https://render.githubusercontent.com/render/math?math=n_i%20%3D%20%282%5C%20prime512%5C%20p_i%20%2B%201%29%282%5C%20prime512%5C%20q_i%20%2B%201%29" />

After simple transformations one has:

<img src="https://render.githubusercontent.com/render/math?math=n_i%20-%201%20%3D%202%5C%20prime512%5C%20%282%5C%20prime512%5C%20p_i%5C%20q_i%20%2B%20p_i%2Bq_i%29" />

So both n have prime512 as a common divisor. We can calculate it by geting 512-bit prime factor of `gcd`:

```python3
dividors = factor( gcd(n1-1,n2-1))
prime512 = next(filter(lambda v, p: len(bin(v)[2:]) == 512))
```

Going further:

<img src="https://render.githubusercontent.com/render/math?math=%5Cfrac%7Bn_i%20-%201%7D%7B2%5C%20prime512%7D%5C%20%3D%202%5C%20prime512%5C%20p_i%5C%20q_i%20%2B%20p_i%2Bq_i" />

<img src="https://render.githubusercontent.com/render/math?math=p_i%2Bq_i" /> as sum of primes is an even number, so we can divide it by 2

<img src="https://render.githubusercontent.com/render/math?math=%5Cfrac%7Bn_i%20-%201%7D%7B4%5C%20prime512%7D%20%3D%20prime512%5C%20p_i%5C%20q_i%20%2B%20%5Cfrac%7Bp_i%2Bq_i%7D2" />

Now we should count bits. Known value (left side) has 1023 bits, prime512 has 512 bits. <img src="https://render.githubusercontent.com/render/math?math=p_i" /> and <img src="https://render.githubusercontent.com/render/math?math=q_i" /> should have 256 bits, sum will have 257, division by 2 gives us 256 bits again. So <img src="https://render.githubusercontent.com/render/math?math=%28p_i%2Bq_i%29%2F2" /> is a lot smaller than prime512. It can be skiped as the rest of division by prime512. We are here for integral values, after all:

<img src="https://render.githubusercontent.com/render/math?math=ls_i%20%3D%20%5Cfrac%7Bn_i-1%7D%7B4%5C%20prime512%7D" />
<img src="https://render.githubusercontent.com/render/math?math=p_i%5C%20q_i%20%3D%20ls_i%5C%20%2F%2Fprime512" />

Do we have to calculate further? To decrypt the flag, we need to find di. To find di, we need to have fii. And what is fii?

<img src="https://render.githubusercontent.com/render/math?math=ni%20%3D%20%282%20prime512%20pi%20%2B%201%29%282%20prime512%20qi%20%2B%201%29" />

<img src="https://render.githubusercontent.com/render/math?math=fi_i%20%3D%202%20prime512%20pi%20%2A%202%20prime512q1%20%3D%204%20prime512%5E2%20pi%20qi" />

And <img src="https://render.githubusercontent.com/render/math?math=p_i%5C%20q_i" /> we already have.

[Solution code](sol.py)
