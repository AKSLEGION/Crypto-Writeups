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

flag=""
part_index=0
flag_part=""

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