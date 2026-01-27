print("Converter")
print("Make conversions:")
print("1 - from int to float")
print("2 - from float to int")
print("3 - from int to str")
print("4 - from float to str")
print("0 - Exit")

while True:
    choice = input("Choose an option (0-4): ")

    if choice == "0":
        print("Goodbye!")
        break

    elif choice == "1":
        num = int(input("Enter an integer: "))
        print(f"{num} as float is {float(num)}")

    elif choice == "2":
        num = float(input("Enter a float: "))
        print(f"{num} as integer is {int(num)}")

    elif choice == "3":
        num = int(input("Enter an integer: "))
        print(f"{num} as string is '{str(num)}'")

    elif choice == "4":
        num = float(input("Enter a float: "))
        print(f"{num} as string is '{str(num)}'")

    else:
        print("Invalid option. Please choose 0-4.")
    
    print() 
