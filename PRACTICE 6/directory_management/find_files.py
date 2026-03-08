import os

path = "directory_management"

print("Text files found:")
counter = 0
for file in os.listdir(path):
    if file.endswith(".txt"):
        print(file)
        counter += 1
if counter == 0:
    print("No files, which end with .txt")

    