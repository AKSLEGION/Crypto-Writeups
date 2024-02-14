import base64
from Crypto.Util.number import *

enc = [base64.b64decode(open(f'conv{i+1}.txt.crypt','rb').read()) for i in range(4)]

key = [0,0,0,0]
key[0] = b'Welcome to our irc server'
key[1] = b' - Hack107 putting t'
key[2] = b'Please send me your '
key[3] = b'Perfect! My new address'

def xor(a,b):
    return b''.join([(i^j).to_bytes(1,'big') for i,j in zip(a,b)])

choice = 0
for i in range(4):
    if len(key[i])>len(key[choice]):
        choice = i

key = key[choice]
f = open("guessed.txt",'wb')
xorkey = xor(enc[choice][0:0+len(key)],key)
for k in range(4):
    f.write(xor(enc[k][0:0+len(key)],xorkey)+b'\n')
