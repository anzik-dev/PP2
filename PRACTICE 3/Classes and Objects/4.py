class Student:
    school = "IT School"   

    def __init__(self, name):
        self.name = name   

student1 = Student("Anzik")
student2 = Student("Dias")

print(student1.school)
print(student2.school)


student1.name = "Ansar"
print(student1.name)


del student1.name
# print(student1.name)  вызовет ошибку