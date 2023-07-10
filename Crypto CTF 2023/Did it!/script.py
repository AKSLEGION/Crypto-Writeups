from pwn import *

host=r'01.cr.yp.toc.tf'
port=11337
r=remote(host,port)

print(r.recvline())
print(r.recvline())
print(r.recvline())

n,l=127,20
dic={}
for i in range(n):
	dic[i]=pow(i,2,n)

list_of_inputs=[]
added_to_list=[False]*n
while added_to_list!=[True]*n:
	input=[]
	collision_check=set()
	count=0
	for i in range(127):
		if added_to_list[i]==True:
			continue
		if dic[i]-1 not in collision_check and dic[i] not in collision_check and dic[i]+1 not in collision_check:
			input.append(i)
			collision_check.add(dic[i])
			collision_check.add(dic[i]+1)
			added_to_list[i]=True
			count+=1
		if count==20:
			break
	list_of_inputs.append(input)

K=[]
for i in range(len(list_of_inputs)):
	s=','.join(map(str,list_of_inputs[i]))
	r.sendline(s.encode())
	did=r.recvline().decode().strip()
	not_in_k=did.lstrip('+ DID = [').rstrip(']')
	lis=list(map(int,not_in_k.split(', ')))
	for num in list_of_inputs[i]:
		if dic[num] not in lis and dic[num]+1 not in lis:
			K.append(num)
			print(f"{num} is in K" )

s=','.join(map(str,K))
r.sendline(s.encode())
r.recvline()
print(r.recvline().decode().strip())
r.close()