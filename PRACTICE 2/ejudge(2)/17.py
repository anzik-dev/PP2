n = int(input())
l = []
for i in range(n):
    b = input().strip()  
    l.append(b)

answer = 0


for num in set(l):
    if l.count(num) == 3:   
        answer += 1

print(answer)
