# Care The Factors !
## Author: D0ppl3gang3r

## Source

- Download the file and decrypt the encrypted file.

### Files: 
- source_thefactors.sage
- flag_thefactors.txt

## Encryption

- The file 'source_thefactors.sage' contained code of an ECC encryption. It was a Discrete Logarithm Challenge

```py
def enc_flag(shared_secret):
	md5 = hashlib.md5()
	md5.update(str(shared_secret).encode())
	key = md5.digest()[:16]
	iv = os.urandom(16)
	cipher = AES.new(key, AES.MODE_CBC, iv)
	ciphertext = cipher.encrypt(pad(flag, 16))
	output = {}
	output['iv'] = iv.hex()
	output['flag'] = ciphertext.hex()
	return output
```
- This part of the code is just for encrypting the flag using the shared_secret and AES encryption

```py
p=1410235279292998784331797202421753874063265295308568058662741299116310072677 
A = getA()
B = getB()
Fp = FiniteField(p)
E = EllipticCurve(Fp, [A, B])
P = E.random_element()
n = randint(2**30, 2**60)
Q = n * P
flag = enc_flag(n)
print(f"{P=}")
print(f"{Q=}")
print(f"{flag=}")
```
- In this portion of the code, 2 numbers were generated A and B which were the parameters for the Elliptic Curve
- `p` is given which is a weak prime since `(p-1)` can be factorised into 8 different primes. So we can apply Pohlig-Hellman Algorithm here.

## Decryption

- First we have to get the parameters A and B.
- We know the equations of Elliptic Curves are of format `y^2 = x^3 + a*x + b`. We have 2 points, so we have x1,x2,y1 and y2. So, this becomes a problem of linear equations.

```py
p = 1410235279292998784331797202421753874063265295308568058662741299116310072677
x1,y1=(406156291172024449433827761031736513098183950832214481256475543523051604042, 937502472800241241676075882016117499207790111193756481427079135615174871684)
x2,y2=(92554882076587701525654416824880284407135974444455993706448015434816328085, 1067245947645250194968549384640439378373660468218406176128671131644883921569)
Ax1B = (y1**2-x1**3)%p
Ax2B = (y2**2-x2**3)%p
A = ((Ax1B-Ax2B)*(pow(x1-x2,-1,p)))%p
B = (Ax1B-A*x1)%p
```
- This gave A = -1 and B = 7

- Now we know the Elliptic Curve, we know the two points, all that's left is to run a discrete log.
- I was facing some difficulties in using the discrete_log function in sagemath. So, I manually wrote the code for discrete_log.

```py
from sage.all import *
from sage.groups.generic import bsgs

def discrete_log(Q, P, order):
    primes = []
    for i in order.factor():
        primes.append(i)
        if len(primes)==9:
            break
    logs = [0] * len(primes)
    for i in range(len(primes)):
        pi,ei = primes[i]
        for j in range(ei):
            logs[i] += bsgs(P * (order // pi), (Q - (P * logs[i])) * (order // (pi ** (j + 1))), (0, pi), operation='+') * (pi ** j)
    return crt(logs, [pow(pi,ei) for (pi, ei) in primes])

K = GF(p)
E = EllipticCurve(K, [A, B])
P = E(x1,y1)
Q = E(x2,y2)
print(n := discrete_log(Q, P, E.order()))
```
- This breaks down the discrete log problem into small sub-problems using the prime factorisation of `(p-1)` and then solves each problem using `baby-step-giant-step` algorithm.
- In the end, it uses `Chinese-Remainder-Theorem` to get the culmination of all those sub-problems, the final discrete log.

```py
def dec_flag(shared_secret):
	md5 = hashlib.md5()
	md5.update(str(shared_secret).encode())
	key = md5.digest()[:16]
	iv = bytes.fromhex(flag['iv'])
	cipher = AES.new(key, AES.MODE_CBC, iv)
	dec = cipher.decrypt(bytes.fromhex(flag['flag']))
	return dec

flag={'iv': '4318aa195451964d2078e230494ef079', 'flag': '75ae6944d3434c9e96affd40c6137bfe23934fddcc6693bdfdd7a1d542f3464a12abc09d87dd0dc8fd860d666dd2b337'}
print(dec_flag(n))
```
- Then I just reversed the `enc_flag()` function to get `dec_flag()` and used the data in 'flag_thefactors.sage' and `n` to get the flag.

### Output
```
1883705452
b'HACKDAY{W34k_EC_W1th_P0hlig_H3llm4n_4TT4cK}\x05\x05\x05\x05\x05'
```

## Flag

The flag is `HACKDAY{W34k_EC_W1th_P0hlig_H3llm4n_4TT4cK}`