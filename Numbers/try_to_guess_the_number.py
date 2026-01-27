import random
print("Game:'Try to guess the number'")
a = random.randint(1,10)
while True:
    b = int(input())
    if a == b:
        print("you win!")
        break
    else:
        print("try again")