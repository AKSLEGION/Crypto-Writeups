PKEY = 55208723145458976481271800608918815438075571763947979755496510859604544396672
ENC = 127194641882350916936065994389482700479720132804140137082316257506737630761

N_E=bin(PKEY)[2:]
N=int(N_E[:-8],2)*2**8
E=int(N_E[-8:],2)*2**8
ENC=ENC*2**8

import math
import sympy
from Crypto.Util.number import *

n=55208723145458976481271800608918815438075571763947979755496510859604544396613
p=188473222069998143349386719941755726311
q=292926085409388790329114797826820624883
phi=(p-1)*(q-1)


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