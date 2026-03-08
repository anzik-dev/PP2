n = int(input())
l = list(map(str, input().split()))
print(max(l, key = len))