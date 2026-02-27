def divisibility(num):
    first = True
    for i in range(0, num + 1, 12):
        if not first:
            print(" ", end="")
        print(i, end="")
        first = False

a = int(input())
divisibility(a)