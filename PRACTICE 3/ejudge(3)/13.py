prime = []
l = list(map(int, input().split()))

for num in l:
    if num < 2:
        continue

    counter = 0
    for j in range(1, num + 1):
        if num % j == 0:
            counter += 1

    if counter == 2:
        prime.append(num)
if len(prime)>0:
    for i in prime:
        print(i, end=" ")
else:
    print("No primes")

