n = int(input())
a = {}

for i in range(n):
    s, x = input().split()
    x = int(x)

    if s not in a:
        a[s] = 0
    a[s] += x

for s in sorted(a):
    print(s, a[s])
