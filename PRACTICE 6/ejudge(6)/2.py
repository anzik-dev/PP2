def is_even(num):
    return num%2 == 0


n = int(input())
l = list(map(int, input().split()))

filtered_numbers = filter(is_even, l)

even_numbers = list(filtered_numbers)
print(len(even_numbers))