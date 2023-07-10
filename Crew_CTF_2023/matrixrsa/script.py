from pwn import *
from Crypto.Util.number import *

host=r'matrixrsa.chal.crewc.tf'
port=20001

while True:
	try:
		r=remote(host,port)

		print(r.recvline())
		print(r.recvline())
		print(r.recvline())
		encflag_0=int(r.recvline().decode().strip(),16)
		encflag_1=int(r.recvline().decode().strip(),16)
		print(f"encflag_0 : {encflag_0}")
		print(f"encflag_1 : {encflag_1}")

		print(r.recvline())
		enc_0=encflag_0
		enc_1=encflag_1*2
		payload_0=hex(enc_0)[2:].encode()
		payload_1=hex(enc_1)[2:].encode()
		r.sendline(payload_0)
		r.sendline(payload_1)

		feedback=r.recvline().decode().strip()
		print(feedback)
		if("size error" in feedback):
			r.close()
			continue
		else:
			break
	except:
		continue

msgintx2=int(r.recvline().decode().strip(),16)
print(f"msgintx2 : {msgintx2}")
msgint=msgintx2//2
padded_flag=long_to_bytes(msgint)
flag=padded_flag.split(b'\x00')[1]
print("\nThe flag is : " + flag.decode().strip())

r.close()