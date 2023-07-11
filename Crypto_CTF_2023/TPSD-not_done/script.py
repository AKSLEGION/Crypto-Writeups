from pwn import *

host=r'05.cr.yp.toc.tf'
port=11137

from Crypto.Util.number import *
from math import *
from sympy import isprime

def find_b(l,r):
	l = round(((2**l+1)//9)**(1/3))
	r = round(((2**r+1)//9)**(1/3))
	for b_ in range(l,r):
        	a = 9*(b_**3)+1
        	if isprime(a):
        		return b_

while True:
	try:
		r=remote(host,port)

		for i in range(9):
			print(r.recvline())

		while True:
			print(r.recvline())
			range_=r.recvline().decode().strip()
			l_r=range_.split('(')[1].split(')')[0]
			left,right=map(int,l_r.split(', '))
			print(left,right)

			b = find_b(left,right)
			P = 9*(b**4)
			Q=-3*b-9*(b**4)
			R=1+9*(b**3)

			s=str(P)+','+str(Q)+','+str(R)
			print(s)
			r.sendline(s.encode())
			print(r.recvline())
	except:
		r.close()
		break