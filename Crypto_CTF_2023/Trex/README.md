# Trex

## Source

The study of Diophantine equations over trex can be significantly more challenging than over the real numbers.

## Exploit

Let's start by understanding the code in trex.py.

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

Now entering the `main()` function
```
def main():
	border = "|"
	pr(border*72)
	pr(border, ".::   Hi all, she DID it, you should do it too! Are you ready? ::.  ", border)
	pr(border, "Welcome to the Ternary World! You need to pass each level until 20  ", border)
	pr(border, "to get the flag. Pay attention that your solutions should be nonzero", border)
	pr(border, "distinct integers. Let's start!                                     ", border)
	pr(border*72)
```
- Prints the welcome text and instructions.

```
	level, step = 0, 19
	while level <= step:
		a = random.randint(2**(level * 12), 2**(level*12 + 12))
		equation = f'x^2 + y^2 - xy = {a}*z^3'
		pr(f"Level {level + 1}: {equation}")
```
- This means that there will be 19 levels in the code, each this it will produce an equation of format `x^2 + y^2 - xy = a * z^3` where a is a random integer which gets higher with levels.

```
		inputs = input().strip().split(",")
		try:
			x, y, z = map(int, inputs)
		except:
			die(border, "Invalid input, Bye!!")
		if check_inputs(x, y, z):
			if check_solution(a, x, y, z):
				pr(border, "Correct! Try the next level :)")
				level += 1
			else:
				pr(border, "You didn't provide the correct solution.")
				die(border, "Better luck next time!")			
		else:
			pr(border, "Your solutions should be non-zero distinct integers")
			die(border, "Quiting...")
		if level == step:
			pr(border, "Congratulations! You've successfully solved all the equations!")
			die(border, f"flag: {flag}")
```
- In every level, based on the value of a, we have to provide values of x,y and z of our choice so that it satisfies `check_inputs(x,y,z)` and `check_solution(a,x,y,z)` then we will get the flag in the last level.

```
def check_inputs(a, b, c):
	if not all(isinstance(x, int) for x in [a, b, c]):
		return False
	if a == 0 or b == 0 or c == 0:
		return False
	if a == b or b == c or a == c:
		return False
	return True

def check_solution(a, x, y, z):
	return (x*x + y*y - x*y - a*(z**3)) == 0
```
- The `check_inputs()` function makes sure all inputs are distinct and none are 0, whereas the `check_solution()` function checks if the values of x,y and z satisfies the given equation.

- **Exploit :** The equation `x^2 + y^2 - xy = a * z^3` can simply be converted to a quadratic equation if we control y and z. `x^2 - xy + y^2 - a*z^3 = 0`.
- It would be easier to make it such that both roots are equal. So, b^2=4ac i.e. `y^2=4*y^2-4*a*z^3` -> `3*y^2 = 4*a*z^3`.
- So, if we take `z = 3*a` , `y = 6*a^2` and `x = -b/2 = y/2 = 3*a^2`.

## Script

### 1.Making the Connection and receiving the introduction
```
from pwn import *

r=remote(r"03.cr.yp.toc.tf",31317)

for i in range(5):
    r.recvline()
```

### 2.Clearing the levels with the derived relations between a, x, y and z
```
for i in range(19):
    n=r.recvline().decode()
    print(n)
    a=int(n.split('=')[1].split('*')[0][1:])
    x=str(3*a**2)
    y=str(6*a**2)
    z=str(3*a)
    payload=(x+','+y+','+z).encode()
    r.sendline(payload)
    r.recvline()
```
- Payload is formed with x,y,z separated by comma and sent as input 19 times

### 3.Getting the flag
```
print(r.recvline())
flag=r.recvline().decode().strip()[2:]
print(flag)
```

## Flag

The flag is `CCTF{T3rn3ry_Tr3x_3Qu4t!0n}`