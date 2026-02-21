students = [
    ("Anzik", 90),
    ("Aruzhan", 85),
    ("Dias", 95)
]

sorted_students = sorted(students, key=lambda x: x[1])

print(sorted_students)