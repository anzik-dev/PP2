a = int(input())
b = list(map(int, input().split()))  
n = 0
for i in b:
    if i>0:
        n+=1
print(n)

