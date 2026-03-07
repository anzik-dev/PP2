string = input().strip().split()
count = 0
for x in string:
    if len(x) == 3:
        count+=1
print(count)