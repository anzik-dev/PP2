
with open("file_handling\data.txt", "a") as file:
    file.write("This line was appended later.\n")
    file.write("Another appended line.\n")

print("New lines appended.\n")


with open("file_handling\data.txt", "r") as file:
    print(file.read())