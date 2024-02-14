import base64

enc = [base64.b64decode(open(f'conv{i+1}.txt.crypt','rb').read()) for i in range(4)]

def xor(a,b):
    return b''.join([(i^j).to_bytes(1,'big') for i,j in zip(a,b)])

f = open('Hack107.txt','wb')
l = min([len(i) for i in enc])
for ind in range(l-6):
    f.write(str(ind).encode()+b'\n')
    for i in range(4):
        xorkey = xor(enc[i][ind:ind+7],b"Hack107")
        for j in range(4):
            f.write(xor(enc[j][ind:ind+7],xorkey)+b'\n')
        f.write(b'\n')
