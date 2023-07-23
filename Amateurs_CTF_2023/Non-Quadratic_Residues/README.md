# Non-Quadratic Residues

## Source

I realized the flaw in my previous system, so now I'll patch it up using my new foolproof system. What previous system? I have no idea but maybe there used to be one??? I still think there's no way you're stealing my flag!

## Encrypt

- The prime generating function
```
def getModPrime(modulus):
    p = getPrime(1024)
    p += (modulus - p) % modulus
    p += 1
    iters = 0
    while not isPrime(p):
        p += modulus
    return p
```
- It basically gets a prime and then rounds up to the next number which leaves remainder 1 when divided by modulus and stops when it gets a prime of that format.

```
difficulty = 210

flag = bytes_to_long(flag)

# no cheeses here!
b = getModPrime(difficulty**10)

c = inverse(flag, b)
n = pow(c, difficulty, b)

with open('output.txt', 'w') as f:
    f.write(f"{n} {b}")
```
- The exponent `e` is 210. `b` replaces the generic RSA `n` as the modulus here. It creates the `n`, the ciphertext as `flag^(-e) mod b` and gives us `n` and `b`.

## Decrypt

- The given information
```
from Crypto.Util.number import *

n = 13350651294793393689107684390908420972977381011191079381202728507002264420264784588373703945341668404762890725356808809021906408198983625375190500172144348596288910240548668158058030780501343680214713780242304547715977777103636873360269427453504233184515002477489763359569764117968027273137245802436961373256
b = 135954424160848276393136392848608760791498666756786983317146989739232222268153235587604168914827859099133726281621143020610041450200631778336472889038077986687446107427527703447531968569919642975653169056203851297117178187249653136191818357235077367060617558261023389453028554177668515375377299577050000000001
```

- Since `e` is so small we can run a sage program to get the roots of this small polynomial.
- Using sage to get all possible numbers such that `num^210 mod b = n`
```
from sage.all import *

F = GF(b)
P.<x> = F[x]
f = x^210-n
l = f.roots()
```
- If you can't run sage, run this code at [Sage Cell Server](https://sagecell.sagemath.org/) to get the list of roots and save it in a py file as a list variable.

- Checking all possible roots saved in `sage_output.py` to see if any of them returns the flag
```
from sage_output import *

for c,_ in l:
	msg = long_to_bytes(pow(c,-1,b))
	if b'amateursCTF{' in msg:
		print("The flag is : " + msg.decode())
		break
```

## Flag

The flag is : `amateursCTF{w3ll_m4yb3_if_th3r3_w3r3_n0_fl4g_to_st3aL_n0_on3_w0uld_st3al_1t!!!!!_lmao_60b15b45}`