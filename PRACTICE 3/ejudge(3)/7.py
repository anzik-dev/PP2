from math import sqrt

a, b = map(int, input().split())
c, d = map(int, input().split())
e, f = map(int, input().split())

answer = sqrt((c - e) ** 2 + (d - f) ** 2)

print(f'({a}, {b})')
print(f'({c}, {d})')
print(f'{answer:.2f}')
