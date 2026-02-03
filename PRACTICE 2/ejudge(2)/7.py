a = int(input())
l = list(map(int, input().split()))  
max_num = max(l)
for i in range(len(l)):
    if l[i] == max_num:
        print(i+1)
        break