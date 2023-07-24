# whiteboard

## Source

Bryan Gao has gotten into the habit of starting with some numbers on the whiteboard, and then writing down the result of applying a function on a set of the numbers on the whiteboard on the whiteboard. See if you're skilled enough at this to achieve flag!

## Problem

```
for i in range(5):
    ok = run_testcase()
    assert ok
```
- There are 5 testcases.

```
def run_testcase():
    goal = gen_goal()
    print(f"Goal: {goal}")

    whiteboard = {my_very_cool_function(167289653), my_very_cool_function(68041722)}  # stO HBD BRYAN GAO Orz
    print(whiteboard)
```
- A `goal` is generated which is the number we need to reach.
- `whiteboard` is created which is a set that initially contains 2 numbers.

```
    for _ in range(1412):
        try:
            a, b = map(int, input("Numbers to combine? ").split())
            assert a in whiteboard and b in whiteboard

            x = 2 * a - b
            whiteboard.add(x)

            if x == goal:
                print("Good job")
                return True

        except:
            print("smh bad input *die*")
            exit("Exiting...")

    return False
```
- We can perform a maximum of 1412 operations in which we choose 2 numbers `a` and `b`, both from the set `whiteboard` and then add `2*a-b` to the set.
- We have to reach the goal in those operations to pass the testcase or we fail.

```
successes = 0
prefixes = ["1", "4", "1", "2"]
suffixes = ["0533", "0708", "1133"]  # skittles1412 birthday Orz... May has 30 days ofc (he claims 12/03 but i call cap)

def gen_goal():
    goal = random.choice(prefixes)
    for i in range(140):
        while (x := random.choice(prefixes)) == goal[-1] and random.randint(1, 5) != 1:
            pass
        goal += x
    goal += random.choice(suffixes)
    return int(goal)
```
- A completely random number of 140 + 4 digits is formed which is the `goal`.
	- The first 140 digits are selected from the list `prefixes`
	- The last 4 digits are selected from the list `suffixes` which is key in the solving procedure.
```
def my_very_cool_function(x):
    return pow(x, 2141, 998244353)
```
- Just a function that takes a number and returns another by `pow(x, 2141, 998244353)`.

## Approach

- Lets start with the numbers that we have in the beginning on our whiteboard. `pow(x := 167289653, 2141, 998244353) = 33` and `pow(x := 68041722, 2141, 998244353) = 8`.

- The only operation we can perform to get new numbers is `2*a-b`. This operation is linear and has 2 important properties:
	1. If we subtract a fixed number `s` from all numbers, i.e. `a = a-s` and `b = b-s`, then `c = 2*a-b` becomes `c_ = 2*(a-s)-(b-s) = 2*a-b-s = c-s`. So, if we pretend all numbers on the whiteboard to be less by a fixed value we can still apply the same operations.
		- *So, we can pretend the 2 numbers already present `{33,8}` to be `{25,0}` by subtracting 8.*
	2. Since the expression is linear if we multiply or divide all numbers with a fixed number `s`, i.e. `a = a//s` and `b = b//s`, then `c = 2*a-b` becomes `c_ = 2*a//s - b//s = (2*a-b)//s = c//s`. So, if we pretend all numbers on the whiteboard to be divided by a fixed value, we can still apply the same operations.
		- *So, we can pretend the 2 numbers `{25,0}` to be `{1,0}` by dividing by 25.*
	3. *If you look at how the `goal` is generated in the `gen_goal()` function, then the last four digits are one of `["0533", "0708", "1133"]`. i.e. if we perform the same operation `x = (x-8)//25` on these suffixes, it will perfectly return an integer since they are of format 8 mod 25.*

- This way we can convert `goal` to a number `bgoal` that has to be reached from the `whiteboard = {1,0}` instead of `whiteboard = {33,8}`.

- Since we have `{1,0}` we can get `-1 = 2*(0)-(1)`. Then we will build the binary of `bgoal` with `0` and `-1`.

- Lets say the binary if `bgoal` is `0b101011`. We will start with `0` and then keep adding one bit from the left. How we can build the binary , is because the operation we are provided with is `2*a-b`.
	- So lets say to get `0b101011` *(last digit is 1)* we will take `a = 0b10101` and `b = -1`. That way `2*a = 0b101010` and on subtracting `-1` it becomes `0b101011`.
	- So lets say to get `0b110100` *(last digit is 0)* we will take `a = 0b11010` and `b = 0`. That way `2*a = 0b110100` and on subtracting `0` it remains `0b110100`.

- We can keep performing these 2 types of operations to build the binary of the goal.

- Counterparts of `1, 0 and -1` in actual `whiteboard` are `33, 8 and -17`. Everytime on sending the numbers we have to keep in mind the real `whiteboard` numbers. S0, we will have to send the previous `n` to multiply by 2 and `8` replacing for `0-bit` or `-17` replacing for `-1-bit`.

## Solution

1. Setting up the connection
```
from pwn import *

host = r'amt.rs'
port = 31694
r = remote(host,port)
```

2. Receiving the goal and preparing the bits of bgoal and hence the list of operations we need to conduct
```
for _ in range(5):
	goal = int(r.recvline().decode().strip().lstrip("Goal: "))
	bgoal = (goal-8)//25
	operation = bin(bgoal)[2:]
```
- We convert the `goal` to `bgoal` which is in the format where `whiteboard` is `{1,0}`.
- `operation` is the list *(in string format)* of bits of `bgoal` in binary format.

3. Adding -17 to the whiteboard to form `1` bits in `bgoal`
```
	r.recv()
	s="8 33"
	r.sendline(s.encode())
	a=8
	b=-17
```

4. Starting with `n = 0` and getting to `bgoal` 1 bit at a time
```
	n=8
	for i in operation:
		s = str(n) + ' '
		if i == '1':
			s += str(b)
			n = 2*n-b
		else:
			s += str(a)
			n = 2*n-a
		r.recv()
		r.sendline(s.encode())
	r.recvline()
```
- We start with `n = 0` which is 8 in the real `whiteboard`
- Then we send `n -17` to add a `1-bit` to `bgoal` or `n 8` to add a `0-bit` to `bgoal`, until we form `bgoal` which is `goal` in the real `whiteboard`

5. Getting the flag
```
r.recvline()
print("The flag is : " + r.recvline().decode().strip())
```
- After reaching the `goal` 5 times we get the `flag`.

## Flag

The flag is : `amateursCTF{hbd_bryan_gao!!!}`