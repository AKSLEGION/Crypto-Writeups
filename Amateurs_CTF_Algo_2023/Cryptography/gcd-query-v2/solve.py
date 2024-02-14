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

print("The flag is : " + flag)