g = 0
n = 0

num = int(input())

for _ in range(num):
    scope, value = input().split()
    value = int(value)

    if scope == "global":
        g += value
    elif scope == "nonlocal":
        n += value

print(g, n)