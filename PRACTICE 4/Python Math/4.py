import random
print(random.random()) 
print(random.randint(1, 10))  
colors = ["red", "blue", "green"]
print(random.choice(colors))
numbers = [1, 2, 3, 4, 5]
random.shuffle(numbers)
print(numbers)