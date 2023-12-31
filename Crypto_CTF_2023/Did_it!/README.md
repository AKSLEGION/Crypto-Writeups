# Did it!

## Source

Finding the intersection among subsets can sometimes be a challenging endeavor, as it requires meticulous comparison and analysis of overlapping elements within each set. But she did it! Try doing it yourself too.

## Exploit

Let's start by understanding the code in did.py.

```
def die(*args):
	pr(*args)
	quit()

def pr(*args):
	s = " ".join(map(str, args))
	sys.stdout.write(s + "\n")
	sys.stdout.flush()

def sc():
	return sys.stdin.buffer.readline()
```

- These 3 functions are used to interact with the user.
- `sc()` takes the input you provide.
- `pr()` prints something.
- `die()` prints something and ends the program.

now entering the `main()` function:

```
border = "+"
pr(border*72)
pr(border, ".::   Hi all, she DID it, you should do it too! Are you ready? ::.  ", border)
pr(border*72)

_flag = False
n, l = 127, 20
N = set(list(range(0, n)))
K = [randint(0, n-1) for _ in range(l)]
cnt, STEP = 0, 2 * n // l - 1
```

the function prints 3 lines and then moves on to define:
1. a boolean `_flag` which checks if it should give you the flag
2. `N`: The integers involved in this program belong to range 0 to 126
3. `K`: a list of 20 random integers from set N that changes with every connection but remains constant throughout the code
4. `cnt` and `STEP` used to confirm that the user can only guess 11 times (2*n//l-1=11)

```
while True:
	ans = sc().decode().strip()
	try:
		_A = [int(_) for _  in ans.split(',')]
		if len(_A) <= l and set(_A).issubset(N):
			DID = did(n, l, K, _A)
			pr(border, f'DID = {DID}')
			if set(_A) == set(K):
				_flag = True
		else:
			die(border, 'Exception! Bye!!')
	except:
		die(border, 'Your input is not valid! Bye!!')
	if _flag:
		die(border, f'Congrats! the flag: {flag}')
	if cnt > STEP:
		die(border, f'Too many tries, bye!')
	cnt += 1
```

- This block of code runs for a maximum of 11 times and lets you send a maximum of 20 numbers from set `N` as input each time.
- The numbers you send as input should be separated by commas and the code will convert it into a list `_A`.
- Then it will run the `did` function.. explained later and print its return.
- **IF your input is the set of all numbers belonging to list `K` then `_flag` will be set and it will give you the flag.**

Now lets understand the did function and how it will help us get the flag.
```
def did(n, l, K, A):
	A, K = set(A), set(K)
	R = [pow(_, 2, n) + randint(0, 1) for _ in A - K]
	return R
```

- This function basically takes A-K , which is the set of all number provided by you in input that do not belong to set K ...say x, then adds x^2 mod(n) or x^2 mod(n) +1 to the list R and returns R.
- Using this we can check for every number given by us in input , if neither x^2 mod(n) nor x^2 mod(n) +1 is in the returned value, then that number is a part of set K and we can save it, to send it in the final input to get the flag.

## Script

Lets start with explaining the script now.

### 1. Setting up the connection:
```
from pwn import *

host=r'01.cr.yp.toc.tf'
port=11337
r=remote(host,port)

print(r.recvline())
print(r.recvline())
print(r.recvline())
```
- **Imports the pwn library and sets up connection to the challenge.**
- **Prints the challenge start message.**

### 2. Preparing a set of inputs:
- It's important to make sure that there are no collisions or we might miss a number that might be in K.
- *Collisions: if dic[a] is k and dic[b] is k+1 : if did returns k+1 in the list, we won't know if a or b doesn't belong to set K.*
```
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
```
- **Creates the dictionary for x to x^2 mod(n).**
- **Creates a list of list of numbers to send as input one at a time.**
- `added_to_list` manages if a number is added to the list. `input` is a list of maximum 20 numbers that is sent to the program as string s. `collision_check` makes sure there are no collisions.

### 3.Submitting numbers to extract numbers in K.
```
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
```
- Sends at most 20 numbers at a time and gets the list returned from did function as lis.
- Then checks for all numbers sent in input if that number is in K (if dic[i] or dic[i]+1 is not in lis) then adds that number to the list K.

### 4.Submitting K and getting the flag.
```
s=','.join(map(str,K))
r.sendline(s.encode())
r.recvline()
print(r.recvline().decode().strip())
r.close()
```

## Flag

The flag is `CCTF{W4rM_Up_CrYpt0_Ch4Ll3n9e!!}`