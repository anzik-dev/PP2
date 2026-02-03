n = int(input())
l = list(map(int, input().split()))
seen = set()
for x in l:
    if x in seen:
        print("NO")
    else:
        print("YES")
        seen.add(x)
