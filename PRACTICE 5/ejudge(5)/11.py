import re
string = input().strip().split()
count = 0
for x in string:
    for j in x:
        match = re.search("[A-Z]",j)
        if match:
            count+=1
print(count)


