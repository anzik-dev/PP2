num =int(input())
fibonacci = []
for i in range(0, num):
    if i == 0:
        fibonacci.append(i)
    if i == 1:
        fibonacci.append(i)
    if i != 0 and i!= 1:
        n = fibonacci[i-1]+fibonacci[i-2]
        fibonacci.append(n)
first = True
for x in range(0, len(fibonacci)):
    if not first:
        print(",", end="")
    print(fibonacci[x], end="")
    first = False

