from Crypto.Util.number import long_to_bytes,bytes_to_long

def P(x):
	return formula(x)
def Q(x):
	return another_formula(x)

n = P(X)*Q(X)
phi = (P(X)-1)*(Q(X)-1)
e = 0x10001
d = pow(e, -1, phi)

print(n)
def encrypt(pt:str, e, n):
	pt = pt[::-1]
	ct = pow(bytes_to_long(pt.encode()), e, n)
	return ct

def decrypt(ct:int, d, n):
	pt = pow(ct, d, n)
	pt = long_to_bytes(pt).decode()
	return pt[::-1]

flag = input("Que souhaitez-vous chiffrer ? ")
print(encrypt(flag, e, n))
