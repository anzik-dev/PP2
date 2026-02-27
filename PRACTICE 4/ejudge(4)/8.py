num = int(input())
primes = []
counter = 0
for i in range(1,num+1):
    for j in range(1,num+1):
        if i%j == 0:
            counter += 1
    if counter == 2:
        primes.append(i)
    counter = 0
first = True
for x in primes:
    if not first:
        print(" ", end="")
    print(x, end="")
    first = False