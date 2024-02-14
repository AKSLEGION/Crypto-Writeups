# Baby Cryptography
## Author: Chelinka

## Source

- Among the exchanges recovered between the Union agents we also saw an encrypted message. He must be talking about something important. That is why we ask you to decipher the communication. We know that the agent knows how to xor and how to count...

- Decrypt the file (which was base64 for portability) FLAG FORMAT : HACKDAY{email}

### Files: 
- secret.txt

## Encryption

- he Challenge only gives us 2 hints: `The agent knows how to xor` and `The agent knows how to count`
- So, It can be fair assumption that the message has been xored and the xor-key is increasing by 1 each time, as in counting.

## Decryption

- Xor is symmetric so all we have to do is take the same xor-keys and repeat the process done by the agent to get the message

```py
import base64

enc = base64.b64decode(open('secret.txt','rb').read())
for i,byte in enumerate(enc):
    print(chr((i^byte)%256),end='')
```

- Here we extracting the encrypted message from the file 'secret.txt' by base64 decoding it.
- Then we are xoring each byte with its index in `enc`. 
- We need to do %256 otherwise the byte will exceed ascii value limit.

### Output
```
Hello W0rm3st3r,

Here are the instructions to follow:
 - You are going to use the usual implant to enter the company's virtual enclosure we talked about last time.
- The implant will be detected after a few days by the Blue Team, which is perfectly normal. This gives us plenty of time to scan the network, as well as the Active Directory behind it.
- Your only objective is to park in the Starbucks opposite the company and collect the data emitted by the implant.
- Once you've completed the scan, or stopped the implant, you'll send us the encrypted data to the following address: C2endpoint@requiemC2.thm.htb.rm.fr

Let's get to work!
```

## Flag

The flag is `HACKDAY{C2endpoint@requiemC2.thm.htb.rm.fr}`