import math
from Crypto.Util.number import *

cipher_hex = open('out.txt','r').read()
ciphertext = bytes.fromhex(cipher_hex)

length = len(ciphertext)
pairs = []

for keylength in range(10,100):
	if length % keylength==0:
		plaintext_len = length//keylength
		if math.gcd(keylength,plaintext_len) == 1:
			pairs.append((keylength,plaintext_len))

for keylength,plaintext_len in pairs:
	if keylength%2 == 0:
		continue
	xored = []
	for i in range(plaintext_len):
		print(i)
		xor = 0
		for j in range(i,length,plaintext_len):
			xor ^= ciphertext[j]
		xored.append(xor)

	flag_end = ord('}')
	for i in range(plaintext_len):
		xor_key = xored[i] ^ flag_end
		msg = b''
		for b in xored[:i+1]:
			msg += long_to_bytes(b ^ xor_key)
		if b'CTF' in msg:
			flag = b'amateursCTF{' + msg.split(b'amateursCTF{')[1]
			print("The flag is : " + flag.decode())
			break
