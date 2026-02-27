x1, y1 = map(float, input().split())
x2, y2 = map(float, input().split())
answer = (x1*y2 + x2*y1)/(y1+y2)
print(f"{answer:.10f} {0:.10f}")