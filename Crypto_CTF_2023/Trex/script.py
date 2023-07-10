from pwn import *

r=remote(r"03.cr.yp.toc.tf",31317)

for i in range(5):
    r.recvline()
    
for i in range(19):
    n=r.recvline().decode()
    print(n)
    a=int(n.split('=')[1].split('*')[0][1:])
    x=str(3*a**2)
    y=str(6*a**2)
    z=str(3*a)
    payload=(x+','+y+','+z).encode()
    r.sendline(payload)
    r.recvline()

print(r.recvline())
flag=r.recvline().decode().strip()[2:]
print(flag)