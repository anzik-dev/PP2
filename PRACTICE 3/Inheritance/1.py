class Person:
    def __init__(self, name):
        self.name = name

    def greet(self):
        print("Hello, my name is", self.name)


class Student(Person):
    pass

student1 = Student("Anzik")
student1.greet()