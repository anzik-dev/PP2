n = int(input())
l = list(map(int, input().split()))
most_frequent = l[0]
max_count = l.count(most_frequent)

for x in l:
    count = l.count(x)
    if count > max_count:
        max_count = count
        most_frequent = x
    elif count==max_count:
        most_frequent = min(most_frequent, x)

print(most_frequent)