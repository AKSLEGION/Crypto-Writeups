# Suction

## Source

The easy suction cryptosystem is designed with a primary focus on simplicity and user-friendliness, employing streamlined algorithms that make encryption straightforward and accessible even for individuals without extensive technical knowledge.

## Encryption

```
def keygen(nbit, r):
	while True:
		p, q = [getPrime(nbit) for _ in '__']
		e, n = getPrime(16), p * q
		phi = (p - 1) * (q - 1)
		if GCD(e, phi) == 1:
			N = bin(n)[2:-r]
			E = bin(e)[2:-r]
			PKEY = N + E
			pkey = (n, e)
			return PKEY, pkey
```
- This function generates 3 primes `p, q` of 128 bits each and `e` of 16 bits.
- It then forms `n = p*q` and then saves all except the last `r=8` bits of `n` and all except the last `r=8` bits of `e` as `PKEY = N + E`.

```
def encrypt(msg, pkey, r):
	m = bytes_to_long(msg)
	n, e = pkey
	c = pow(m, e, n)
	C = bin(c)[2:-r]
	return C
```
- This function encrypts the msg using the rsa formed and returns the encrypted message without the last `r=8` bits and returns the rest as `C`
```
r, nbit = 8, 128
PKEY, pkey = keygen(nbit, r)
print(f'PKEY = {int(PKEY, 2)}')
FLAG = flag.lstrip(b'CCTF{').rstrip(b'}')
enc = encrypt(FLAG, pkey, r)
print(f'enc = {int(enc, 2)}')
```
- The leet code inside the flag is encrypted.
- We are given the decimal converted form of `PKEY` and `C`

## Decryption

**We can just go through all `2**8 * 2**8 * 2**8` possibilities created by the loss of bits and perform rsa decryption when possible.**

### 1. Getting n : decrypt_1.py

```
PKEY = 55208723145458976481271800608918815438075571763947979755496510859604544396672
ENC = 127194641882350916936065994389482700479720132804140137082316257506737630761

N_E=bin(PKEY)[2:]
N=int(N_E[:-8],2)*2**8
E=int(N_E[-8:],2)*2**8
ENC=ENC*2**8
```
- Extracts the leftmost digits of `n, e` and `enc` and sets the last 8 digits as 0 by multiplying 2**8.

```
import sympy
import math

primes=set()
for i in range(10**6):
	if sympy.isprime(i):
		primes.add(i)

possible_n=set()

for i in range(2**8):
	n=N+i
	composite=False
	for prime in primes:
		if n%prime==0:
			composite=True
			break
	if not composite:
		possible_n.add(n)

for i in possible_n:
	print("n : " + str(i))
```
- Imports sympy and runs the first block of code to get all primes under 10**6
- Goes through all the possible n by changing the last 8 bits and checks if they are divisible by any prime under 10**6 which are max 20 bit long primes.
- Since `n = p*q` where p and q are 128 bit primes , n can't be divisible by any primes in that range, so we get rid of those n's and print the possible ones.

```
Output:
n : 55208723145458976481271800608918815438075571763947979755496510859604544396577
n : 55208723145458976481271800608918815438075571763947979755496510859604544396643
n : 55208723145458976481271800608918815438075571763947979755496510859604544396613
n : 55208723145458976481271800608918815438075571763947979755496510859604544396583
n : 55208723145458976481271800608918815438075571763947979755496510859604544396589
n : 55208723145458976481271800608918815438075571763947979755496510859604544396751
n : 55208723145458976481271800608918815438075571763947979755496510859604544396783
n : 55208723145458976481271800608918815438075571763947979755496510859604544396723
n : 55208723145458976481271800608918815438075571763947979755496510859604544396667
n : 55208723145458976481271800608918815438075571763947979755496510859604544396571
n : 55208723145458976481271800608918815438075571763947979755496510859604544396633
n : 55208723145458976481271800608918815438075571763947979755496510859604544396603
```

### 2. Finding true n

The fastest way here would be to take each n and factorise them using the websites 'http://factordb.com/' or 'https://www.dcode.fr/prime-factors-decomposition' and check if there are only 2 primes both 128 bit long, that is n and the factors are p and q.

```
n=55208723145458976481271800608918815438075571763947979755496510859604544396613
p=188473222069998143349386719941755726311
q=292926085409388790329114797826820624883
```

### 3. Performing rsa decryption

```
PKEY = 55208723145458976481271800608918815438075571763947979755496510859604544396672
ENC = 127194641882350916936065994389482700479720132804140137082316257506737630761

N_E=bin(PKEY)[2:]
N=int(N_E[:-8],2)*2**8
E=int(N_E[-8:],2)*2**8
ENC=ENC*2**8
```
- Explained earlier. To get the base value of e and c..

```
import math
import sympy
from Crypto.Util.number import *

n=55208723145458976481271800608918815438075571763947979755496510859604544396613
p=188473222069998143349386719941755726311
q=292926085409388790329114797826820624883
phi=(p-1)*(q-1)
```

- Imports the required libraries and gets `n,p,q and phi`

```
for i in range(2**8):
	e=E+i
	if not sympy.isprime(e):
		continue
	d=pow(e,-1,phi)
	for j in range(2**8):
		c=ENC+j
		m=pow(c,d,n)
		flag=long_to_bytes(m)
		try:
			print("The flag is CCTF{" + flag.decode() + "}")
		except:
			continue
```
- For all possibilities of `e` checks if `e` is a prime as we know from the encryption script. If it is, then it finds `d` and continues with all possibilities of `c`.
- For all possibilities of `c` it finds out flag by rsa decryption: `m = pow(c,d,n)` then checks if all bytes in that flag are alphabets or numbers of symbols. If it is, then it might be the actual flag so it prints the flag encased in CCTF{}.

## Flag

The flag is CCTF{6oRYGy&Dc$G2ZS}