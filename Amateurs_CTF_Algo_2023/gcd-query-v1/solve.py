from pwn import *

host = r'amt.rs'
port = 31692

r = remote(host,port)

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

print("The flag is : " + r.recvline().decode())