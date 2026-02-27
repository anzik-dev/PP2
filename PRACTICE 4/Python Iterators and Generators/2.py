numbers = [10, 20, 30]

for num in numbers:
    print(num)
print("-" * 10)

it = iter(numbers)

while True:
    try:
        print(next(it))
    except StopIteration:
        break