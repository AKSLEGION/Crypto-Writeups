# ASlv1

## Source

Despite their large size, corporations like ASIv1 often exhibit a surprising tendency to rely on vulnerable cryptosystems in an attempt to encrypt their secret financial transactions, inadvertently leaving themselves open to potential security breaches and exposing the fragility of their approach.

## Encryption

```
from Crypto.Util.number import *
from flag import flag
```
```
seed = flag.lstrip(b'CCTF{').rstrip(b'}')
R, S = asiv_prng(seed)

f = open('output.txt', 'w')
f.write(f'R = {R}\nS = {S}')
f.close()
```
- **Imports the `flag` from an external file. Extracts the leet string from the `flag` as `seed`.**
- **Encodes the `flag` with function `asiv_prng` and writes in the return to `output.txt`.**

- **Encryption functions:**
```
def base(n, l):
    D = []
    while n > 0:
        n, r = divmod(n, l)
        D.append(r)
    return ''.join(str(d) for d in reversed(D)) or '0'

def asiv_prng(seed):
	l = len(seed)
	_seed = base(bytes_to_long(seed), 3)
	_seed = [int(_) for _ in _seed]
	_l = len(_seed)
	R = [[getRandomRange(0, 3) for _ in range(_l)] for _ in range(_l**2)]
	S = []
	for r in R:
		s = 0
		for _ in range(_l):
			s += (r[_] * _seed[_]) % 3
		# s += getRandomRange(0, 3)
		s %= 3
		S.append(s)
	return R, S
```
- The base function simply converts the number `n` to base `l` and returns the list of the digits. *divmod returns a tuple of quotient and remainder.*
- The `asiv_prng` function encrypts the seed as follows:
	- It takes the `seed` converts it into integer in base 3 and forms a list `_seed` which is the list of digits of the integer.
	- It then creates a list `R` which consists of _l^2^ lists of the same length as `_seed` filled with random digits 0,1 and 2 (base 3 digits).
	- Then it perform modular matrix multiplication on `_seed` and `R` to get `S = R * _seed^T^ ` and returns `R, S`.

## Decryption

*This form of encryption only uses modular matrix arithmetics, so it can be broken using elementary modular matrix operations on the equation `S = R * _seed^T^ `.*

If we can convert the matrix R into:
```
| 1 0 0 0 0 0 0 ... 0 | row 1
| 0 1 0 0 0 0 0 ... 0 | row 2
| 0 0 1 0 0 0 0 ... 0 | row 3
| ................... |
| 0 0 0 0 0 0 0 ... 1 | row _l
| 0 0 0 0 0 0 0 0 0 0 | row _l+1
| 0 0 0 0 0 0 0 0 0 0 | row _l+2
| ................... | down to row _l^2^
```
then the resulting matrix S from the equation `S = R * _seed^T^ ` will have the first _l elements of `S` as `_seed` and the rest elements 0.

We can convert `R` to this form by the same method we use to inverse a matrix, by keeping R[i][i] as 1 and applying row addition to convert the rest of R[j][i] to 0.

- Let's understand decrypt.py

### 1. Extracting R and S from output.txt
```
import os

old_name=r'.\output.txt'
new_name=r'.\output.py'

os.rename(old_name, new_name)

import output

R=output.R
S=output.S
```
- Renames output.txt into output.py using os module and extracts R and S from it.

### 2. Matrix Row Reduction
```
_l=len(R[0])

for i in range(_l):
    count=0
    while(R[i][i]==0):
        count+=1
        R=R[:i]+R[i+1:]+[R[i]]
        S=S[:i]+S[i+1:]+[S[i]]
        if(count>_l**2):
            print("BAD")
            break
    if R[i][i]==2:
        for j in range(i,_l):
            R[i][j]=(R[i][j]*2)%3
        S[i]=(S[i]*2)%3
    for j in range(_l**2):
        if j==i:
            continue
        x=R[j][i]//R[i][i]
        if(x==0):
            continue
        for k in range(i,_l):
            R[j][k]=(R[j][k]-x*R[i][k])%3
        S[j]=(S[j]-x*S[i])%3
```
- In each step of reducing a column it makes sure R[i][i] is 1.
	- If it is 2, then multipies all numbers in the row by 2 mod 3 to make it 1.
	- If it is 0, then sends that row to the end of the matrix until it gets a 1 or 2.
- Then it performs elementary row reduction operation to convert the rest of the column to 0.

### 3. Getting the flag
```
_seed=S[:_l]

m=0
for i in range(110):
    m*=3
    m+=_seed[i]

from Crypto.Util.number import *

seed=long_to_bytes(m).decode()
print("The flag is : CCTF{"+ seed +"}")
```
- Gets the first `_l` digits which is the `_seed` and converts it into bytes to get the flag.

## Flag

The flag is `CCTF{3Xpl0i7eD_bY_AtT4ck3r!}`