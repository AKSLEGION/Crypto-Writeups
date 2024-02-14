# The Fish Trap
## Author: ZEN

## Source

- A file corrupted by the Syndicat was transmitted to us. Apparently, it would contain important information about the Syndicat to allow justice to identify them. Decode the message from the file to retrieve what it said.

- Download the source flag and adapt it to decrypt the flag next to it

### Files: 
- corruptedfile

## Encryption

- The challenge name is `The Fish Trap` which suggests its a Fish Cipher. On searching, the format of text in the corruptedfile turned out to be of Deadfish Language.

## Decryption

- On Using dcode.fr to decrypt the text, it gave some space separated numbers

### Output
```
110 101 103 113 104 101 131 173 122 60 104 137 120 110 61 123 110 61 116 107 137 61 123 137 64 127 63 123 60 115 63 175
```

- On closer inspection, these numbers are in octal base.
- Decoding that gave the flag

## Flag

The flag is `HACKDAY{R0D_PH1SH1NG_1S_4W3S0M3}`