n = int(input())
l = sorted(set(map(int, input().split())))

first = True
for x in l:
    if not first:
        print(" ", end="")
    print(x, end="")
    first = False