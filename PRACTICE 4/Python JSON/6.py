import json

with open("PRACTICE 4\Python JSON\sample-data.json", "r") as file:
    data = json.load(file)

students = data["students"]

# вывести имена
for student in students:
    print(student["name"])

# найти средний балл
total = sum(student["grade"] for student in students)
average = total / len(students)

print("Average:", average)