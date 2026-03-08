import shutil


shutil.copy("file_handling\data.txt", "file_handling\data_copy.txt")


shutil.copy("file_handling\data.txt", "file_handling\data_backup.txt")

print("File copied and backup created.")