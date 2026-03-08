n = int(input())
l1 = list(map(str, input().split()))
l2 = list(map(str, input().split()))

dictionary = dict(zip(l1,l2))

a = input()
try:
    print(dictionary[a])
except KeyError:
    print("Not found")