n = int(input())
a = {}

for i in range(1, n + 1):
    s = input().strip()
    if s not in a:
        a[s] = i

for s in sorted(a):
    print(s, a[s])
