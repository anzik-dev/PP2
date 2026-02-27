import math

r = float(input())
x1, y1 = map(float, input().split())
x2, y2 = map(float, input().split())

dx = x2 - x1
dy = y2 - y1

a = dx * dx + dy * dy
b = 2 * (x1 * dx + y1 * dy)
c = x1 * x1 + y1 * y1 - r * r

D = b * b - 4 * a * c

segment_length = math.sqrt(a)

if D < 0:

    if x1 * x1 + y1 * y1 <= r * r:
        print(segment_length)
    else:
        print(f"{0:.10f}")
else:
    sqrtD = math.sqrt(D)
    t1 = (-b - sqrtD) / (2 * a)
    t2 = (-b + sqrtD) / (2 * a)

    left = max(0, min(t1, t2))
    right = min(1, max(t1, t2))

    if left > right:
        print(f"{0:.10f}")
    else:
        result = (right - left) * segment_length
        print(f"{result:.10f}")