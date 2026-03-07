import string
string = input()
l = []
flag = False
for x in string:
    if x.isdigit():
        flag = True
        l.append(x)
    else:
        flag = False
if len(l)>0:
    for num in l:
        print(num, end=" ")
else:
    print()
    