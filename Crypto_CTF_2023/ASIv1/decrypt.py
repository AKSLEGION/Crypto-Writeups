import os

old_name=r'.\output.txt'
new_name=r'.\output.py'

os.rename(old_name, new_name)

import output

R=output.R
S=output.S

_l=len(R[0])

for i in range(_l):
    count=0
    while(R[i][i]==0):
        count+=1
        R=R[:i]+R[i+1:]+[R[i]]
        S=S[:i]+S[i+1:]+[S[i]]
        if(count>_l**2):
            print("BAD")
            break
    if R[i][i]==2:
        for j in range(i,_l):
            R[i][j]=(R[i][j]*2)%3
        S[i]=(S[i]*2)%3
    for j in range(_l**2):
        if j==i:
            continue
        x=R[j][i]//R[i][i]
        if(x==0):
            continue
        for k in range(i,_l):
            R[j][k]=(R[j][k]-x*R[i][k])%3
        S[j]=(S[j]-x*S[i])%3

_seed=S[:_l]

m=0
for i in range(110):
    m*=3
    m+=_seed[i]

from Crypto.Util.number import *

seed=long_to_bytes(m).decode()
print("The flag is : CCTF{"+ seed +"}")