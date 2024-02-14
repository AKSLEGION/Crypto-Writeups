# gcd-query-v2

## Source

I thought that skittles1412's querying system wasn't optimized enough, so I created my own. My system is so much more optimized than his!

## Problem

- *Its similar to gcd-query-v1.*
```
#!/usr/local/bin/python
from flag import flag
from math import gcd
from Crypto.Util.number import getRandomInteger

x = getRandomInteger(128)
```
- A random number of 128 bits `x` is generated.
```
for i in range(16):
    try:
        n, m = map(int, input("n m: ").split())
        assert m > 0
        print(gcd(x + n, m))
    except:
        print("bad input. you *die*")
        exit(0)
if int(input("x: ")) == x:
    print(flag)
else:
    print("get better lol")
```
- We can run 16 comparisions in which we send two numbers `n` and `m` and we get the gcd of `(x+n)` and `m`. Then we have to guess `x` correctly to get the `flag`.

## Approach

- *The same as gcd-query-v1.*

- The key to this approach is that.
	- The gcd of two numbers is a factor of those numbers.
	- The factor of a number is less than or equal to the number. *except 0*
- Lets fix `m` as a large number that will provide gcds and make `n` to be a negative number so that we will always get the gcd of some number `(x-n)` less than `x` and `m`.
- So the gcd of `(x-n)` and `m` is less than or equal to `(x-n)`. So `x-n -gcd >= 0` in each iteration. So, if we start with `n = 0` and keep repeating this operation: 
	- We get the gcd and subtract that from n, so new n becomes `-n-gcd` in absolute value terms.
	- We keep repeating this until `x -n-gcd` becomes 0, i.e. the gcd values returned is `m`.
- Then we will have `x = n + gcd` and we can run more blank operations to complete the `for i in range(16)` loop and then submit `x` to complete the testcase.

## Solution

1. Preparing the connection and an optimal `m`
```
from pwn import *

host=r'amt.rs'
port=31693

import sympy
import sys
sys.set_int_max_str_digits(0)

m=1
for i in range(50):
	if sympy.isprime(i):
		m*=pow(i,128)
````
- I chose `m` to be the product of high powers of some primes so that the gcd can be higher is each case. *Since number of attempts is less, we want the gcd to be as big as possible to get to the number.*
- `sys.set_int_max_str_digits(0)` allows us to send huge numbers as strings.

2. Executing the approach to get the number
```
while True:
	r=remote(host,port)

	num=0
	for i in range(16):
		r.recv()
		s=str(-num)+' '+str(m)
		r.sendline(s.encode())
		g=int(r.recvline().decode().strip())
		if(g==m):
			continue
		num+=g
	r.recv()
	r.sendline(str(num).encode())

	flag = r.recvline().decode().strip()
	r.close()
	if flag != 'get better lol':
		break
```
- We start with `m` as prepared and `n = 0`.
- Then we execute our approach by sending `-n m` to get the gcd and add that to `n` until we reach `g == m`.
- Then we send the the number we guessed.
- *I have put this inside a while loop because this method is quite probabilistic and we can't be sure we will reach the number is only 16 iterations. So, until we get the flag this code keeps retrying.*

3. Getting the flag
```
print("The flag is : " + flag)
```

## Flag

The flag is : `amateursCTF{crt_really_is_too_op...wtf??!??!?!?must_be_cheating!!...i_shouldn't've_removed_query_number_cap.}`