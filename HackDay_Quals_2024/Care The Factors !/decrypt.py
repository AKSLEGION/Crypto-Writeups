from sage.all import *
from sage.groups.generic import bsgs
import hashlib
from Crypto.Cipher import AES

p = 1410235279292998784331797202421753874063265295308568058662741299116310072677
x1,y1=(406156291172024449433827761031736513098183950832214481256475543523051604042, 937502472800241241676075882016117499207790111193756481427079135615174871684)
x2,y2=(92554882076587701525654416824880284407135974444455993706448015434816328085, 1067245947645250194968549384640439378373660468218406176128671131644883921569)
Ax1B = (y1**2-x1**3)%p
Ax2B = (y2**2-x2**3)%p
A = ((Ax1B-Ax2B)*(pow(x1-x2,-1,p)))%p
B = (Ax1B-A*x1)%p
K = GF(p)
E = EllipticCurve(K, [A, B])
P = E(x1,y1)
Q = E(x2,y2)

def discrete_log(Q, P, order):
    primes = []
    for i in order.factor():
        primes.append(i)
        if len(primes)==9:
            break
    logs = [0] * len(primes)
    for i in range(len(primes)):
        pi,ei = primes[i]
        for j in range(ei):
            logs[i] += bsgs(P * (order // pi), (Q - (P * logs[i])) * (order // (pi ** (j + 1))), (0, pi), operation='+') * (pi ** j)
    return crt(logs, [pow(pi,ei) for (pi, ei) in primes])

print(n := discrete_log(Q, P, E.order()))

def dec_flag(shared_secret):
	md5 = hashlib.md5()
	md5.update(str(shared_secret).encode())
	key = md5.digest()[:16]
	iv = bytes.fromhex(flag['iv'])
	cipher = AES.new(key, AES.MODE_CBC, iv)
	dec = cipher.decrypt(bytes.fromhex(flag['flag']))
	return dec

flag={'iv': '4318aa195451964d2078e230494ef079', 'flag': '75ae6944d3434c9e96affd40c6137bfe23934fddcc6693bdfdd7a1d542f3464a12abc09d87dd0dc8fd860d666dd2b337'}
print(dec_flag(n))