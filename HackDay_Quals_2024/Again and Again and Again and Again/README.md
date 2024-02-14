# Again and Again and Again and Again
## Author: Chelinka

## Source

- Among the exchanges recovered between the Union agents we also saw an encrypted message. He must be talking about something important. That is why we ask you to decipher the communication. We know that the agent knows how to xor and how to count...

- Decrypt the file (which was base64 for portability) FLAG FORMAT : HACKDAY{email}

### Files: 
- conversation.zip
    - conv1.txt.crypt
    - conv2.txt.crypt
    - conv3.txt.crypt
    - conv4.txt.crypt

## Encryption

- The title says again and again .. 4 times, and there are 4 encrypted files in the zip file. That would suggest that the same encryption is being used for all 4 messages.
- We can see from the padding that the ciphertexts are base64 encoded, which on decoding gives byte strings of different length.
- So, it can be a fair assumption that the messages are strings of different length which have been xored with the same key, for all 4 messages.. hence the title, again and again...
- Another hint provided is that the messages are about "Hack107" which should be a plaintext in one of the messages.

## Decryption

### Finding the index

- The first step would be to find the position where "Hack107" is present.
- To do so, we will guess the presence of "Hack107" at every index in every ciphertext.
    - Then in every instance we will get the xorkey by xoring the selected section of the selected ciphertext with "Hack107". 
    - We will use the same xorkey on all 4 ciphertexts to get the selected section of the original messages assumed in that instance.
    - If all 4 sections match the format of actual english message strings we will deem that to be the right position for "Hack107"

```
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
```
- Here i am printing all possibilities of 7 length sections of the messages by assuming the position for "Hack107".

### Output

```
3
Hack107
come to
J}k.b!6
Mkmz0d

come to
Hack107
ase sen
fect! M

J}k.b!6
ase sen
Hack107
Owe?cu

Mkmz0d
fect! M
Owe?cu
Hack107
```

- For index 3 to 9 in the second message, "Hack107" fits providing proper strings for the rest 3 messages too.

### Guessing the rest of the messages



## Flag

The flag is `HACKDAY{C2endpoint@requiemC2.thm.htb.rm.fr}`