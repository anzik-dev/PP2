import re
string = input()
x = re.match("Hello", string)
if x:
    print("Yes")
else:
    print("No")


