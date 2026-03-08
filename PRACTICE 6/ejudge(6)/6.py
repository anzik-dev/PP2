n = int(input())
l = list(map(int, input().split()))
if all(n >= 0 for n in l):
    print("Yes")
else:
    print("No")