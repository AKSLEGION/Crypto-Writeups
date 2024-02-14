fleg = "610c6115651072014317463d73127613732c73036102653a6217742b701c61086e1a651d742b69075f2f6c0d69075f2c690e681c5f673604650364023944"

fleg_bytes = bytes.fromhex(fleg)
flag = ""

for i in range(len(fleg_bytes)):
	if i%2==0:
		flag+=chr(fleg_bytes[i])
	else:
		flag+=chr(fleg_bytes[i]^fleg_bytes[i-1])

print(f"The flag is : {flag}")