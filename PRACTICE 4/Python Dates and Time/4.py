from datetime import datetime

d1 = datetime(2026, 2, 27, 10, 0, 0)
d2 = datetime(2026, 2, 28, 12, 30, 0)

difference = d2 - d1

print(difference)          # 1 day, 2:30:00
print(difference.days)     # 1
print(difference.seconds)  # 9000