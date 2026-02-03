a = int(input())
l = list(map(int, input().split()))  
max_num = max(l)
min_num = min(l)
for i in range(len(l)):
    if l[i] == max_num:
        l[i] = min_num
for i in l:
    print(i, end= " ")