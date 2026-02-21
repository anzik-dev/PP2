class Student:
    def __init__(self, name):
        self.name = name

    def greet(self):
        print("Hello, my name is", self.name)

student1 = Student("Anzik")
student1.greet()