# matrixrsa

## Source

I create an extension of RSA. Can you test it?

Author : kiona

## Exploit

This challenge is a combination of matrix exponentiation with modular arithmetics.

Starting with the main() function
```
def main():
    try:
        banner = "Welcome to matrix RSA world"
        print(banner)

        (p,q), n = keygen()

        paddedflag = pad(FLAG, 2*size-1)
        assert unpad(paddedflag) == FLAG
        paddedflagint = bytes_to_long(paddedflag)
        encflag_0, encflag_1 = encrypt(paddedflagint, n)
        assert decrypt((encflag_0, encflag_1), (p, q)) == paddedflagint
        print("Here is encrypted flag(enc_0, enc_1):")
        print(long_to_bytes(encflag_0).hex())
        print(long_to_bytes(encflag_1).hex())
```

- The code starts with generating 2 large primes and creating n=p*q
- Then it pads the flag with random bytes and converts it into int and encrypts it.

Understanding the Encryption:
```
def encrypt(msgint, n):
    a = bytes_to_long(os.urandom(int(2*size-1)))
    # sympy.FiniteField treats non-prime modulus instance as Z/nZ
    Zmodn = FiniteField(n)
    mat = DomainMatrix([
            [Zmodn(a), Zmodn(msgint)],
            [Zmodn(0), Zmodn(a)]
        ], (2, 2), Zmodn)

    enc = mat**int(e)
    enc_0 = int(enc[0,0].element.val)
    enc_1 = int(enc[0,1].element.val)
    return (enc_0, enc_1)
```

- The encrypt() function starts with a 2x2 matrix:
```
| a , msg |
| 0 ,  a  |
```
- Then it raises that matrix to power e=65537 while keeping in under mod n and it becomes:
```
| a^e , e*a^(e-1)*msg |
| 0   ,      a^e      |
```

- Then the function returns the first 2 values of the matrix i.e. a^e and e*a^(e-1)*msg
- Now the thing that makes this exploit possible is that enc_1 = e\*a^(e-1)\*msg is directly proportional to msg. So, on encrypting msg\*2 the return of encryption will be enc_1 = e\*a^(e-1)\*msg\*2 = 2\*enc_1 for msg

- Lets look at the rest of the main() function:
```
	while True:
            print("Please input encrypted message(enc_0, enc_1):")
            enc_0 = bytes_to_long(bytes.fromhex(input('>> ')))
            enc_1 = bytes_to_long(bytes.fromhex(input('>> ')))
            if enc_0 >= n or enc_1 >= n:
                print("size error")
                continue
            if (enc_0 * encflag_1 - enc_1 * encflag_0) % n == 0:
                print("Do not input related to encrypted flag")
                continue
            dec = decrypt((enc_0, enc_1), (p, q))
            if FLAG in long_to_bytes(dec):
                print("Do not input encrypted flag")
            else:
                print("Here is decrypted message:")
                print(long_to_bytes(int(dec)).hex())
    except:
        quit()
```
- So, the code gives us unlimited number of attempts to guess values of enc_0 and enc_1 and it will return us the corresponding value of msgint by a decrypt function which is secret to us.
- However we can't resend the encrypted data we got at the start of the code directly and not with the relation (enc_0 * encflag_1 - enc_1 * encflag_0) % n == 0

- So , as discussed above .. if we send encflag_0 and twice encflag_1 as input .. it will decrypt it and return to us 2*msgint as the decrypted message in the form of hex. All we have to do is divide that by 2 and convert it into bytes to get the flag.
- \*There is a condition that enc_0 and enc_1 should be less than n. So, on sending 2\*encflag_2, the value might cross the limit and there will be a size error. Then we can simply refresh the connection to get a new n and new encoded values. There is a 50% possibility of us getting the flag.

## Script

### 1.Defining the connection
```
from pwn import *
from Crypto.Util.number import *

host=r'matrixrsa.chal.crewc.tf'
port=20001
```
- We simply import all required libraries and initialise the credentials for connection

### 2.Getting the encoded values and Sending the exploit
```
while True:
	try:
		r=remote(host,port)

		print(r.recvline())
		print(r.recvline())
		print(r.recvline())
		encflag_0=int(r.recvline().decode().strip(),16)
		encflag_1=int(r.recvline().decode().strip(),16)
		print(f"encflag_0 : {encflag_0}")
		print(f"encflag_1 : {encflag_1}")

		print(r.recvline())
		enc_0=encflag_0
		enc_1=encflag_1*2
		payload_0=hex(enc_0)[2:].encode()
		payload_1=hex(enc_1)[2:].encode()
		r.sendline(payload_0)
		r.sendline(payload_1)
```
- As discussed we get encflag_0 and encflag_1 and then send the former with twice the value of the latter as inputs.
- The try block is there just in case we hit EOF error in the connection.

### 3.Getting the feedback of size issue
```
		feedback=r.recvline().decode().strip()
		print(feedback)
		if("size error" in feedback):
			r.close()
			continue
		else:
			break
	except:
		continue
```
- We recieve the next line which says "size error" if enc_1 was greater than n, in which case we close the connection and refresh it since this code is in a infinite while loop.
- In case it doesnt say size error, out exploit has been successful so we move forward with the process.

### 4.Getting the flag
```
msgintx2=int(r.recvline().decode().strip(),16)
print(f"msgintx2 : {msgintx2}")
msgint=msgintx2//2
padded_flag=long_to_bytes(msgint)
flag=padded_flag.split(b'\x00')[1]
print("\nThe flag is : " + flag.decode().strip())

r.close()
```
- After confirming that we can move forward with the program we get 2*msgint as predicted, then we divide it by 2 to get msg and convert it into bytes, which will give us the padded_flag. We extract the flag from it knowing that it starts after the byte b'\x00'.

## Flag

The flag is : crew{h4rd_70_53cur3_f0r_m47r1x_r54}