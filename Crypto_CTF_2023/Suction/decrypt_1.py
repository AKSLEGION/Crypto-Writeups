PKEY = 55208723145458976481271800608918815438075571763947979755496510859604544396672
ENC = 127194641882350916936065994389482700479720132804140137082316257506737630761

N_E=bin(PKEY)[2:]
N=int(N_E[:-8],2)*2**8
E=int(N_E[-8:],2)*2**8
ENC=ENC*2**8

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