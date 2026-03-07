import re
a = input()
string = ""
pattern = re.compile(r"^[0-9]+$")
for x in a:
    match = re.sub(pattern, x*2, x)
    string+=match
print(string)