n = int(input())
l1 = list(map(int, input().split()))
l2 = list(map(int, input().split()))

dot_product = sum(a*b for a, b in zip(l1, l2))

print(dot_product)