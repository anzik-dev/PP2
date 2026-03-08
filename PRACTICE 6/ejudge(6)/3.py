n = int(input())
l = input().strip().split()
l_new = enumerate(l)
for index, value in l_new:
    print(f"{index}:{value}", end = " ")