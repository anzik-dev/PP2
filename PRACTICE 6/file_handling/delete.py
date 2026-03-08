import os

file_name = "file_handling\data_copy.txt"
file_name_1 = "file_handling\data_backup.txt"


if os.path.exists(file_name):
    os.remove(file_name)
    print("File deleted successfully.")
else:
    print("File does not exist.")


if os.path.exists(file_name_1):
    os.remove(file_name_1)
    print("File deleted successfully.")
else:
    print("File does not exist.")