import base64

enc = base64.b64decode(open('secret.txt','rb').read())
for i,byte in enumerate(enc):
    print(chr((i^byte)%256),end='')