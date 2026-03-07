import re
a = input()
b = input()

x = re.findall(b,a)
print(len(x))