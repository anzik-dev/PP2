import re
string = input()
pattern = "\S+@\S+\.\S+"
x = re.search(pattern, string)
if x:
    print(x.group())
else:
    print("No email")
