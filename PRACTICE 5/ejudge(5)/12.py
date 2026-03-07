import re
a = input()
l = re.findall("[0-9]+[0-9]", a)
for x in l:
    print(x,end=" ")
