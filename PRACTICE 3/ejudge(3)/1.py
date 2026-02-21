num = input()
counter = True
for i in range(0,len(num)):
    x = int(num[i])
    if x%2 == 0:
        counter = True
    else:
        counter = False
        break
if counter == True:
    print("Valid")
else:
    print("Not valid")
