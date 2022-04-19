from pwn import *

# This allow for some networking magic
sni_a = {
    "server_hostname":"rs-ayyy-how-you-doin.tamuctf.com"
}
p = remote("tamuctf.com", 443, ssl=True, sni="rs-ayyy-how-you-doin")

## YOUR CODE GOES HERE
p.interactive()
