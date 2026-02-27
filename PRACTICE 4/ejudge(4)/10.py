def lim(array, num):

    array_str = " ".join(map(str, array))

    return " ".join([array_str] * num)

l = list(map(str, input().split()))
k = int(input())

print(lim(l, k))