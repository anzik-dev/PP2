n = int(input())
l = list(map(int, input().split()))
sum_of_x = 0
for x in l:
    sum_of_x += x**2
print(sum_of_x)