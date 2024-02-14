from pwn import *

host = r'amt.rs'
port = 31694
r = remote(host,port)

for _ in range(5):
	goal = int(r.recvline().decode().strip().lstrip("Goal: "))
	bgoal = (goal-8)//25
	operation = bin(bgoal)[2:]
	r.recv()
	s="8 33"
	r.sendline(s.encode())
	a=8
	b=-17
	n=8
	for i in operation:
		s = str(n) + ' '
		if i == '1':
			s += str(b)
			n = 2*n-b
		else:
			s += str(a)
			n = 2*n-a
		r.recv()
		r.sendline(s.encode())
	r.recvline()

r.recvline()
print("The flag is : " + r.recvline().decode().strip())