n, l, r = map(int, input().split())
original = list(map(int, input().split()))

with_positions = original[l-1:r]  
      
with_positions.reverse()          


original[l-1:r] = with_positions

for i in original:
    print(i, end=" ")
