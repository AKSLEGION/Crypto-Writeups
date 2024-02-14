# Compact XORs

## Source

I found some hex in a file called fleg, but I'm not sure how it's encoded. I'm pretty sure it's some kind of xor...

## Decryption

```
610c6115651072014317463d73127613732c73036102653a6217742b701c61086e1a651d742b69075f2f6c0d69075f2c690e681c5f673604650364023944
```
- We have been given the hex of the encrypted flag and the hint from the source is that xor has been used.

### 1. Looking for a pattern
- On converting the hex into bytes format and printing the text:
```
>>> print(bytes.fromhex("610c6115651072014317463d73127613732c73036102653a6217742b701c61086e1a651d742b69075f2f6c0d69075f2c690e681c5f673604650364023944"))
```
- We get a series of bytes where every alternative character seems to coincide with the pattern of the flag `amateursCTF{...}`
```
>>> b'a\x0ca\x15e\x10r\x01C\x17F=s\x12v\x13s,s\x03a\x02e:b\x17t+p\x1ca\x08n\x1ae\x1dt+i\x07_/l\ri\x07_,i\x0eh\x1c_g6\x04e\x03d\x029D'
```

### 2. Checking the xor for the even place bytes
- The even placed bytes should be `_m_t_u_s_T_{`
- The byte in 2nd place is b'\x0c' which would be xor(b'm',xorkey[0]). That makes the xorkey[0] to be b'a'.
- On making similar computation for the next even places we get xorkey[1] = b'a', b'e', b'r'... which are the odd places bytes one place before the bytes we are checking.
- So, every even place byte has simply been xored with the byte before them to create `fleg`.

### 3. Xoring back
```
fleg = "610c6115651072014317463d73127613732c73036102653a6217742b701c61086e1a651d742b69075f2f6c0d69075f2c690e681c5f673604650364023944"

fleg_bytes = bytes.fromhex(fleg)
flag = ""

for i in range(len(fleg_bytes)):
	if i%2==0:
		flag+=chr(fleg_bytes[i])
	else:
		flag+=chr(fleg_bytes[i]^fleg_bytes[i-1])

print(f"The flag is : {flag}")
```
- Xor is self reversing so we simply have to xor every even placed bytes with the byte before it and leave the odd placed bytes alone.

## Flag

The flag is : `amateursCTF{saves_space_but_plaintext_in_plain_sight_862efdf9}`