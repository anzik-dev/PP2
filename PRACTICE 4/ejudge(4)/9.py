num = int(input())
first = True
for i in range(0, num+1):
    if not first:
        print(" ", end="")
    print(2**i,end="")
    first = False