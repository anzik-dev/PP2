a = int(input())
n = 1
l = []

while n <= a:  
    l.append(n)
    n *= 2

print(*l)    
