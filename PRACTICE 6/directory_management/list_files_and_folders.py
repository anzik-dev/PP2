import os

path = "directory_management"

items = os.listdir(path)

print("Files and folders in", path)
for item in items:
    print(item)