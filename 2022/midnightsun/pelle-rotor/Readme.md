# Pelle's rotor supported arithmetic

## Challenge

Script file [pelles_rotor_supported_arithmetic.py](pelles_rotor_supported_arithmetic.py)

## TL;TR;

Encrypting at least 2 sets of messages: <img src="https://render.githubusercontent.com/render/math?math=m_3%20%3D%20m_2%5C%20m_1" />  we can find <img src="https://render.githubusercontent.com/render/math?math=N" />  `k*N = gcd(c1_1*c1_2-c1_3, c2_1*c2_2-c2_3)`, and get ride of `k` by dividing the result by small primes.
Having <img src="https://render.githubusercontent.com/render/math?math=N" /> we retrive $d$ digit by digit:
 <img src="https://render.githubusercontent.com/render/math?math=msg%5E%7B10%5C%20d_r%7D%20%3D%20%5Cfrac%7B%20c_%7Bi%2B1%7D%2BkN%7D%7Bmsg%5E%7Bdigit%7D%7D" />  <img src="https://render.githubusercontent.com/render/math?math=c_i%5E%7B10%7D%20%3D%20msg%5E%7Bdigit%5C%2010%5E%7BdigitCount%7D%7D%5C%20msg%5E%7B10%5C%20d_r%7D" /> 
## Solution

I solved this challenge after the CTF.

The script allows us the opportunity to encrypt our messages using d, the modular multiplicative inverse of e. We can encrypt more times than d has digits. This gives us a spare to calculate N. 

How to find N?
 <img src="https://render.githubusercontent.com/render/math?math=c_1%5C%20c_2%20%3D%20m_1%5Ed%5C%20m_2%5Ed%20%3D%20%28m_1%5C%20m_2%29%5Ed%20%3D%20c_3" /> For modulo operation:
 <img src="https://render.githubusercontent.com/render/math?math=%28m_1%5Ed%29%5C%20mod%5C%20%20N%5C%20%28m_2%5Ed%29%5C%20mod%5C%20N%20%3D%20%28m_1%5C%20m_2%29%5Ed%5C%20mod%5C%20N%20%2B%20kN" />  <img src="https://render.githubusercontent.com/render/math?math=c_1%5C%20c_2%20-%20c_3%20%3D%20%20kN" /> 
If we choose good messages so that <img src="https://render.githubusercontent.com/render/math?math=c_1%5C%20c_2%20%3E%20N" /> 
Prepare 2 or 3 sets of messages. Using `gcd(k1*N, k2*N)` we should get N. But sometimes `gcd` still returns muiltiple of N. For assurance, one may try to divide it by small primes.

So we have N.

Next d.

"Size" (number of digits) of $d$ cannot be greater than the number of digits of N. We can send the same message to encryption with i = [0... digits count for N] and compare results. When it will be equal to cipher for i=0. And we have the "size" of <img src="https://render.githubusercontent.com/render/math?math=d" /> 

Next, what are adjacent ciphers look like:

 <img src="https://render.githubusercontent.com/render/math?math=d_%7Bi%7D%20%3D%20digit%5C%2010%5E%7BdigitCount-1%7D%20%2B%20d_r" />  <img src="https://render.githubusercontent.com/render/math?math=d_%7Bi%2B1%7D%20%3D%2010%5C%20d_r%20%2B%20digit" />  <img src="https://render.githubusercontent.com/render/math?math=c_%7Bi%7D%20%3D%20msg%5E%7Bd_%7Bi%7D%7D%20%3D%20msg%5E%7Bdigit%5C%2010%5E%7BdigitCount-1%7D%7D%5C%20msg%5E%7Bd_r%7D" />  <img src="https://render.githubusercontent.com/render/math?math=c_%7Bi%2B1%7D%20%3D%20msg%5E%7Bd_%7Bi%2B1%7D%7D%20%3D%20msg%5E%7B10%5C%20d_r%7D%5C%20msg%5E%7Bdigit%7D" />  <img src="https://render.githubusercontent.com/render/math?math=msg%5E%7Bdigit%7D" /> for small msg is so small that iterating we can find $k$ that would fullfill condition:
 <img src="https://render.githubusercontent.com/render/math?math=c_%7Bi%2B1%7D%20%2B%20kN%5C%20mod%5C%20%20msg%5E%7Bdigit%7D%20%3D%3D%200" /> and next:
 <img src="https://render.githubusercontent.com/render/math?math=msg%5E%7B10%5C%20d_r%7D%20%3D%20%5Cfrac%7B%20c_%7Bi%2B1%7D%2BkN%7D%7Bmsg%5E%7Bdigit%7D%7D" /> Using $c_1$ to 10th power (**all modulo N**) we can compare cipher with out calculation for choosen $digit$:
 <img src="https://render.githubusercontent.com/render/math?math=c_i%5E%7B10%7D%20%3D%20msg%5E%7Bdigit%5C%2010%5E%7BdigitCount%7D%7D%5C%20msg%5E%7B10%5C%20d_r%7D" /> 
So I check all digits, which one meets the condition.

[Solution](sol.py)
