import math

r = float(input())
x1, y1 = map(float, input().split())
x2, y2 = map(float, input().split())

# расстояние между A и B
distAB = math.hypot(x2 - x1, y2 - y1)

# расстояния до центра
dA = math.hypot(x1, y1)
dB = math.hypot(x2, y2)

# Проверка пересечения отрезка с кругом

dx = x2 - x1
dy = y2 - y1

a = dx*dx + dy*dy
b = 2*(x1*dx + y1*dy)
c = x1*x1 + y1*y1 - r*r

D = b*b - 4*a*c

intersects = False
if D >= 0:
    sqrtD = math.sqrt(D)
    t1 = (-b - sqrtD)/(2*a)
    t2 = (-b + sqrtD)/(2*a)
    if max(0, min(t1,t2)) <= min(1, max(t1,t2)):
        intersects = True

if not intersects:
    print(f"{distAB:.10f}")
else:
    theta = math.acos((x1*x2 + y1*y2) / (dA*dB))
    alpha = math.acos(r / dA)
    beta = math.acos(r / dB)
    arc = r * (theta - alpha - beta)

    tangentA = math.sqrt(dA*dA - r*r)
    tangentB = math.sqrt(dB*dB - r*r)

    answer = tangentA + tangentB + arc
    print(f"{answer:.10f}")