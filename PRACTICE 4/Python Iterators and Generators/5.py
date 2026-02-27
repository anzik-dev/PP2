nums = [x * 2 for x in range(5)]
print(nums)
nums = (x * 2 for x in range(5))
print(nums)
print(type(nums)) 
for value in nums:
    print(value)