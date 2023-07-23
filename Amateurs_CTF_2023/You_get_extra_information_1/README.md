# You get extra information 1

## Source

![Source jpg](source.jpg)

## Encrypt

```
from Crypto.Util.number import *
from flag import flag

p = getPrime(512)
q = getPrime(512)
n = p*q
p = p + q
e = 0x10001

extra_information = p + q
ptxt = bytes_to_long(flag)
c = pow(ptxt, e, n)

with open('output.txt', 'w') as f:
    f.write(f"n: {n}\nc: {c}\ne: {e}\nextra_information: {extra_information}")
```
- Rsa Key is created by generating 2 primes `p` and `q` and creating `n = p*q` and selecting `e = 0x10001`
- We are provided with `n, c, e` and `extra_information = new_p + q = p + 2*q`

## Decrypt

- We have `n = p*q` and `extra_information = p + 2*q` , so we can get `(p - 2*q)^2^ = (p + 2*q)^2^ - 8*p*q`

```
from Crypto.Util.number import *

n = 83790217241770949930785127822292134633736157973099853931383028198485119939022553589863171712515159590920355561620948287649289302675837892832944404211978967792836179441682795846147312001618564075776280810972021418434978269714364099297666710830717154344277019791039237445921454207967552782769647647208575607201
c = 55170985485931992412061493588380213138061989158987480264288581679930785576529127257790549531229734149688212171710561151529495719876972293968746590202214939126736042529012383384602168155329599794302309463019364103314820346709676184132071708770466649702573831970710420398772142142828226424536566463017178086577
e = 65537
extra_information = 26565552874478429895594150715835574472819014534271940714512961970223616824812349678207505829777946867252164956116701692701674023296773659395833735044077013
```
- The Given Information

```
import gmpy2
gmpy2.get_context().precision=10000

q2_minus_p = int(gmpy2.root(extra_information**2-8*n,2))

p = (extra_information - q2_minus_p)//2
q = (extra_information-p)//2
```
- Getting `2*q - p` by the method mentioned above and `p` and `q` from it.

```
phi = n-p-q+1
d = pow(e,-1,phi)
m = pow(c,d,n)

print("The flag is : " + long_to_bytes(m).decode())
```
- Decrypting the RSA since we now have the two primes.

## Flag

The flag is : `amateursCTF{harder_than_3_operations?!?!!}`