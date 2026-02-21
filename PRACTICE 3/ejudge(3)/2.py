def only_235(n):
    for p in [2,3,5]:
        while n%p == 0:
            n//=p
    return "Yes" if n == 1 else "No"
a = int(input())
print(only_235(a))