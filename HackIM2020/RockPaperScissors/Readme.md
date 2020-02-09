# RockPaperScissors 


## Challenge

> To get the flag you have to beat us in rock paper scissors but to make it fair we used a commitment based scheme.
> 
> nc crypto1.ctf.nullcon.net 5000
> 
> file: rps.py

### Solution

The story is: every turn the program choose random 16 bytes and adds *move* and calculate the hash. This 3 hashes are shuffled and served to us in final order. Let us analyse hash method: 

```python
def hash(data):
    state = bytearray([208, 151, 71, 15, 101, 206, 50, 225, 223, 14, 14, 106, 22, 40, 20, 2])
    data = pad(data, 16)
    data = group(data)
    for roundkey in data:
        for _ in range(round):
            state = repeated_xor(state, roundkey)
            for i in range(len(state)):
                state[i] = sbox[state[i]]
            temp = bytearray(16)
            for i in range(len(state)):
                temp[p[i]] = state[i]
            state = temp
    return hex(bytes_to_int(state))[2:]
```

Our data is allways *[16b secret][1b move]*, so after padding: *[16b secret][1b move][15b * \x0f]*. This is split to 16b parts (roundkeys). First part is out secret, but the second can be one of 3: 
```b'r'+15*b'\x0f'```, ```b'p'+15*b'\x0f'``` or ```b's'+15*b'\x0f'```.
For every move fisrt 16b are the same so first iteration of hash calculation per group (roundkey) gives us the same ```status value```. Then our paths split. But nothing fancy all operation can be reversed till this point. So I 'half'-reverse calculations for each of 3 movements. 

```python
...
# q - inverted p
# qbox - inverted sbox

def revert(hash: str, proposal_key: bytes):
    value = int(hash, 16)
    state = long_to_bytes(value)
    for _ in range(16):
        tmp = bytearray(16)
        for i in range(len(state)):
            tmp[q[i]] = state[i]
        state = tmp
        for i in range(len(state)):
            state[i] = qbox[state[i]]
        state = repeated_xor(state, proposal_key)
    return (chr(proposal_key[0]), bytes_to_long(state))

...
```

So for every given hash, I get 3 proposition (*move*, ```state``` after hashing unknown secret part). I need only to find ```state``` value between hashes.

```python
...

def sol(hashes):
    res = []
    for h in hashes:
        rkey = [b'p' + b'\x0f' * 15, 
                b'r' + b'\x0f' * 15, 
                b's' + b'\x0f' * 15]
        calc = [revert(h, key) for key in rkey]
        res.append(calc)

    for i1 in range(3):
        for i2 in range(3):
            for i3 in range(3):
                if res[0][i1][1] == res[1][i2][1] and res[1][i2][1] == res[2][i3][1]: 
                    return res[0][i1][0]
    return None

...

```

