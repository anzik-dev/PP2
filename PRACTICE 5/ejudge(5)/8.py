import re
s = input()
d = input()
x = re.split(d, s)
first = True
for value in x:
    if not first:
        print(",", end='')
    print(value, end="")
    first = False
