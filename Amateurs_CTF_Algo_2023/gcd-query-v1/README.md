# gcd-query-v1

## Source

I wonder if this program leaks enough information for you to get the flag with less than 2048 queries... It probably does. I'm sure you can figure out how.

## Problem

```
#!/usr/local/bin/python
from flag import flag
from math import gcd
from Crypto.Util.number import getRandomInteger


for i in range(10):
    x = getRandomInteger(2048)
```
- The number of testcases is 10. In every testcase a random integer of 2048 bits `x` is generated, which we have to guess.

```
    for i in range(1412):
        try:
            n, m = map(int, input("n m: ").split())
            assert m > 0
            print(gcd(x + n, m))
        except:
            print("bad input. you *die*")
            exit(0)
    if int(input("x: ")) != x:
        print("get better lol")
        exit(0)

print(flag)
```
- We can run 1412 comparisions in which we send two numbers `n` and `m` and we get the gcd of `(x+n)` and `m`. Then we have to guess `x` and on passing it 10 times we will get the `flag`.

## Approach

- The key to this approach is that.
	- The gcd of two numbers is a factor of those numbers.
	- The factor of a number is less than or equal to the number. *except 0*
- Lets fix `m` as a large number that will provide gcds and make `n` to be a negative number so that we will always get the gcd of some number `(x-n)` less than `x` and `m`.
- So the gcd of `(x-n)` and `m` is less than or equal to `(x-n)`. So `x-n -gcd >= 0` in each iteration. So, if we start with `n = 0` and keep repeating this operation: 
	- We get the gcd and subtract that from n, so new n becomes `-n-gcd` in absolute value terms.
	- We keep repeating this until `x -n-gcd` becomes 0, i.e. the gcd values returned is `m`.
- Then we will have `x = n + gcd` and we can run more blank operations to complete the `for i in range(1412)` loop and then submit `x` to complete the testcase.

## Solution

1. Setting up the connection
```
from pwn import *

host = r'amt.rs'
port = 31692

r = remote(host,port)
```

2. Approaching `x`
```
for _ in range(10):
	m = pow(2,2048)
	num = 0
	for i in range(1412):
		r.recv()
		payload = str(-num)+' '+str(m)
		r.sendline(payload.encode())
		gcd = int(r.recvline().decode().strip())
		if(g != m):
			num += g
	r.recv()
	r.sendline(str(num).encode())
```
- We start with m just higher than what `x` can be and `n = 0`.
- Then we execute our approach by sending `-n m` to get the gcd and add that to `n` until we reach `g == m`.
- Then we send the the number we guessed.

3. Getting the flag
```
print("The flag is : " + r.recvline().decode())
```

## Flag

The flag is : `amateursCTF{probabilistic_binary_search_ftw}`