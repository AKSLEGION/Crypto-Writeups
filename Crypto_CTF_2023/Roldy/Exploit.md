# Roldy

## Source

Roldy, once regarded as a reliable cryptosystem library, has unfortunately emerged as one of the most vulnerable and compromised systems in recent times, leaving users exposed to significant security risks.

## Exploit

Let's start by understanding the code in Roldy.py.

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
def main():
	border = "|"
	pr(border*72)
	pr(border, " Welcome to Roldy combat, we implemented an encryption method to    ", border)
	pr(border, " protect our secret. Please note that there is a flaw in our method ", border)
	pr(border, " Can you examine it and get the flag?                               ", border)
	pr(border*72)

	pr(border, 'Generating parameters, please wait...')
	p, k1, k2 = [getPrime(129)] + [getPrime(64) for _ in '__']
	C = encrypt(flag, key, (p, k1, k2))
```

the function prints 6 lines and then moves on to define:
1. `p,k1 and k2` : a 129 bit prime and 2- 64 bit primes
2. `C` : The encrypted flag.

```
	while True:
			pr("| Options: \n|\t[E]ncrypted flag! \n|\t[T]ry encryption \n|\t[Q]uit")
			ans = sc().decode().lower().strip()
			if ans == 'e':
				pr(border, f'encrypt(flag, key, params) = {C}')
			elif ans == 't':
				pr(border, 'Please send your message to encrypt: ')
				msg = sc().rstrip(b'\n')
				if len(msg) > 64:
					pr(border, 'Your message is too long! Sorry!!')
				C = encrypt(msg, key, (p, k1, k2))
				pr(border, f'C = {C}')
			elif ans == 'q':
				die(border, "Quitting ...")
			else:
				die(border, "Bye ...")
```

- This block of code runs infinitely and lets us interact with the program to get the encrypted flag or encrypt a message sent by the user.

- The Encrypt function:
```
def encrypt(msg, key, params):
	if len(msg) % 16 != 0:
		msg += (16 - len(msg) % 16) * b'*'
	p, k1, k2 = params
	msg = [msg[_*16:_*16 + 16] for _ in range(len(msg) // 16)]
	m = [bytes_to_long(_) for _ in msg]
	inra = ValueRange(0, 2**128)
	oura = ValueRange(k1 + 1, k2 * p + 1)
	_enc = enc(key, in_range = inra, out_range = oura)
	C = [_enc.encrypt(_) for _ in m]
	return C
```
- It takes the message and breaks it into blocks of 16 characters (padding if necessary), then encrypts each block separately and returns the values in an array `C`.

- **Exploit :** On entering `"CCTF"` in the input we found that its encrypted value has the first few digits in common with the encrypted value of the flag's first block, and on entering `"CCTF{"` we found that the number of common digits increased. 
- Also since the encrypt function treats them as `"CCTF****************"` and `"CCTF{***************"`, the integer value of 2nd string is greater and the encrypted value of 2nd string was also greater
- So, it was safe to assume that the encryption was based on ascii value of the string, and we can guess the string by trial and error and comparision

## Script

Lets start with explaining the script now.

### 1. Setting up the connection and Preparing functions to interact:
```
from pwn import *

host=r'02.cr.yp.toc.tf'
port=31377

def options():
    for i in range(4):
        r.recvline()
        
def sendstring(string):
    r.sendline(b't')
    r.recvline()
    r.sendline(string.encode())
    x=r.recvline().decode()
    return int(x.split('[')[1].split(']')[0])
```
- Imported the pwn library and initialised the connection credentials.
- The `options()` function receives the 4 options in this line of code : `pr("| Options: \n|\t[E]ncrypted flag! \n|\t[T]ry encryption \n|\t[Q]uit")`
- The `sendstring()` function chooses the `[T]ry encryption` option and sends the string we want to encrypt. It also receives, extracts and returns the encrypted value of the string we sent.

### 2. Preparing the global variables for flag and its running block
```
flag=""
part_index=0
flag_part=""
```
- `flag` saves the blocks of flag that we have extracted completely.
- `part_index` holds which index block of the flag we are currently working on.
- `flag_part` holds the progress on the current flag part.

### 3. Starting the connection and getting the flag.
```
while True:
	try:
		flag_encrypted=[]
		r=remote(host,port)
		for i in range(6):
			r.recvline()

		options()
		r.sendline(b'e')
		encrypted=r.recvline().decode().strip()
		enc_numbers=encrypted.split('[')[1].split(']')[0]
		flag_encrypted=list(map(int,enc_numbers.split(', ')))
		n=flag_encrypted[part_index]
```
- *The code is looped with a try and except: continue condition because this program takes a long time to execute and connection breaks before it finishes. So, we refresh the connection every time which holding on to the 3 global variables to measure progress.*
- The connection is made and the welcome message is received, then we ask for the encrypted flag and extract the array from the encrypt function from the return. Since we are working on one block of the flag at a time, we initialise `n` as the encoded value of flag's `part_index` indexed block.

### 4. Implementing binary search to get the next character:
```
		while len(flag_part)<16:
			low=32
			high=127
			while True:
				mid=(low+high)//2
				char=chr(mid)
				options()
				m=sendstring(flag_part+char)
				if(m>n):
					high=mid
					continue
				else:
					char=chr(mid+1)
					options()
					m_=sendstring(flag_part+char)
					if(m_>n):
						flag_part+=chr(mid)
						print(flag+flag_part)
						break
```
- Since we know the encryption is based on ascii, we run comparisions:
	- Let the flag be `"abcdefghijklmnop"` and we send `"abcd"` , then our input will be encrypted as `"abcd************"` whose ascii value is lower, so we can assume as long as the value is lower we can go up with the next character's ascii value.
	- And if its higher , like "abcdf" then we have to go lower.
	- In case of `"abcde"` which will be encoded as `"abcde***********"` it is lesser in comparision to the flag encrypted and for `"abcdf"` it will be higher , so when we hit enc(flag_part+char)<enc(flag)<enc(flag_part+char+1) we know we have found the next character.
- So, using binary search this way, we find the character which makes the string we are building just less than the flag, then we move forward to the next character.

### 5. Complications: '*' isn't the lowest character:
```
					else:
						if low==127:
							flag_part=flag_part[:-1]+chr(ord(flag_part[-1])+1)
							flag_part+='!'
							print(flag+flag_part)
							break
						if high==32:
							flag=flag[:-1]+chr(ord(flag[-1])+1)
							flag_part+='!'
							print(flag+flag_part)
							break
						low=mid+1
						continue
```
- The character '!' is used in flags too and its ascii value is less than that of '*'. So, lets say the `flag_part` is `"d3s3rv!ng"`, on reaching the 6th character it will determine that `"d3s3ru"` is in the `flag_part`.
	- This is because `"d3s3rv!*********"` is lesser than `"d3s3rv********"` and `"d3s3ru********"` is just lesser than `"d3s3rv!*********"` which is what our code was checking.
- But after determining 6 characters as `"d3s3ru**********"` our program will get to the 2nd character and it won't be able to find '!' since we have already hit the wrong character 'u'. So, the mid value will keep on increasing until it hits the upper limit 127.
- When it hits 127, we can determine that the character is '!' and the last character we found should be increased by 1.

### 6. Breaking the loop and getting the flag:
```
			if flag_part[-1]=='}':
				break
		flag+=flag_part
		flag_part=''
		part_index+=1

		if flag[-1]=='}':
			break
	except:
		continue

print(f"The flag is : {flag}")
```
- The innermost loop breaks everytime we get the next character.
- The next loop breaks everytime we reach 16 characters or get the '}' character which is the closing of the flag, getting us a `flag_part`.
- In the outer loop we add the `flag_part` to the `flag` and update the `part_index`. This loop breaks when we have hit the ending of the flag which is the '}' character.
- Then we print the flag.

## Flag

The flag is `CCTF{Boldyreva_5ymMe7rIC_0rD3r_pRe5Erv!n9_3nCryp7i0n!_LStfig9TM}`