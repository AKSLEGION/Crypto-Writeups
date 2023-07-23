# OwO time pad

## Source

One time pad best cipher. It's unbreakable! Hmm what's the point of it if I have to give you the key though...?

## Encrypt

```
import os
import random
from Crypto.Util.strxor import strxor
from math import gcd

with open('secret.txt', 'rb') as f:
    plaintext = f.read()
```
- The code gets the `plaintext` and sets up for the encryption.

```
    keylength = len(plaintext)
    while gcd(keylength, len(plaintext)) > 1:
        keylength = random.randint(10, 100)
    key = os.urandom(keylength)
```
- It keeps choosing random lengths for `key` until it is co-prime to the length of `plaintext` and then forms a random `key`.

```
    key = key * len(plaintext)
    plaintext = plaintext * keylength
    ciphertext = strxor(plaintext, key)
    with open('out.txt', 'w') as g:
        g.write(ciphertext.hex())
```
- It then repeats the `key` and `plaintext` until they become of same length.
- Then it xors the bytes of both strings and gives us the hex of the `ciphertext`

## Decrypt

- The Given Information
```
import math
from Crypto.Util.number import *

cipher_hex = open('out.txt','r').read()
ciphertext = bytes.fromhex(cipher_hex)

length = len(ciphertext)
```

- Finding all possible key lengths
```
pairs = []

for keylength in range(10,100):
	if length % keylength==0:
		plaintext_len = length//keylength
		if math.gcd(keylength,plaintext_len) == 1:
			pairs.append((keylength,plaintext_len))
```
- We check for each keylength possible if it is co-prime with the corresponding plaintext length and save the cases which satisfy.

```
for keylength,plaintext_len in pairs:
	if keylength%2 == 0:
		continue
	xored = []
	for i in range(plaintext_len):
		print(i)
		xor = 0
		for j in range(i,length,plaintext_len):
			xor ^= ciphertext[j]
		xored.append(xor)
```
- This piece of codes xors all bytes where `plaintext[i]` would be present.
	- If `keylength` is odd then the number of occurences of `plaintext[i]` will be odd hence the final `xor` will be the xor of all bytes in the original `key` and `plaintext[i]`.
	- However if `keylength` is even, it will just be the xor of all bytes in the original `key` and hence we will lose the plaintext byte. So, we will skip this situation.
- The `xored` list will store the final `xor`s for each byte in the plaintext.

```
	flag_end = ord('}')
	for i in range(plaintext_len):
		xor_key = xored[i] ^ flag_end
		msg = b''
		for b in xored[:i+1]:
			msg += long_to_bytes(b ^ xor_key)
		if b'CTF' in msg:
			flag = b'amateursCTF{' + msg.split(b'amateursCTF{')[1]
			print("The flag is : " + flag.decode())
			break
```
- We know that the flag is of the format `amateursCTF{...}`. So, for all possible indices, we will assume `plaintext[i]` to be '}'.
- Then we will get the `xor_key` which is the xor of all bytes in the original `key` by `xor_key = xored[i] ^ ord('}')`.
- Since all numbers in the list `xored` is the xor of `xor_key` and `plaintext[i]`, we will reverse it by xoring every element with `xor_key` again until the bytes where we know the flag ends, i.e. `i`.
- We will continue this for all indices until we get the flag.

## Flag

The flag is : `amateursCTF{M4yb3_H4v3_b3tt3r_0tP_3ncrYpt10n_n3X7_t1m3_l0L!!_a585b81b}`
