# AES

## Challenge

[aes-2.py]('aes-2.py') gets a random 32 bytes 'alice' value and encrypts it by secret random 16 bytes key and two IVs. We know 'alice' and its encrypted value. We are asked to provide a value that is encrypted with the same keys produces a value with the same hash that encrypted 'alice'.

## Solution

Let's start with the hash function. The script XORs every 16 bytes of encrypted value and calculates the hash. We cannot use 'alice' value because it is checked. So our encrypted value should have 16 bytes sections that give 0 after XOR.

Analyze encrypt function:

|   | a | b | c | d | <<- known values
|---|---|---|---|---| ---
XOR| iv1 | a'' | b'' | c'' |
ENC:| a' | b' | c' | d' |
XOR| iv2 | a' | b' | c' |
ENC:| a'' | b'' | c'' | d'' | <<- known values 

A little bit of thinking and we can do something like this:

|   | ali         | ce          | crypt_ce | d      | ENC(0) | ENC(0) ^ ce ^ crypted_ali
|---|---          |---          |---       |---     |---     |---|
XOR | iv1         | crypted_ali | crypt_ce | d      | ENC(0) | ENC(0)
ENC: | ali'        | ENC(ce ^ crypted_ali)| **ENC(0)**   | ENC(0) | ENC(0) | **ENC(ce ^ crypted_ali)**
XOR | iv2         | ali'        | **ENC(ce ^ crypted_ali)**| ENC(0) | ENC(0) | **ENC(0)**
ENC: | crypted_ali | crypt_ce    | d        | ENC(0) | ENC(0) |  d

[sol.py]('sol.py')