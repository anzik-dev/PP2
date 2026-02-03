a = int(input())
l = list(map(int, input().split()))  
l.sort()
for i in range(len(l)-1, -1, -1):
    print(l[i], end =" ")