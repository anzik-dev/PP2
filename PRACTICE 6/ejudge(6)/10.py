n = int(input())
l = list(map(int, input().split()))

counter = sum(map(bool, l))
print(counter)