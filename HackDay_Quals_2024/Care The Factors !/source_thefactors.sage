
from Crypto.Util.number import *
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from random import randint
import hashlib
import os

flag =b"HACKDAY{R3D4CT3D_BY_CRYPT0_COMMUNITY}"

def getA():
	# You have to find it yourself /:
	pass

def getB():
	# You have to find it yourself /:
	pass

def enc_flag(shared_secret):
	md5 = hashlib.md5()
	md5.update(str(shared_secret).encode())
	key = md5.digest()[:16]
	iv = os.urandom(16)
	cipher = AES.new(key, AES.MODE_CBC, iv)
	ciphertext = cipher.encrypt(pad(flag, 16))
	output = {}
	output['iv'] = iv.hex()
	output['flag'] = ciphertext.hex()
	return output

p=1410235279292998784331797202421753874063265295308568058662741299116310072677 
A = getA()
B = getB()
Fp = FiniteField(p)
E = EllipticCurve(Fp, [A, B])
P = E.random_element()
n = randint(2**30, 2**60)
Q = n * P
flag = enc_flag(n)
print(f"{P=}")
print(f"{Q=}")
print(f"{flag=}")