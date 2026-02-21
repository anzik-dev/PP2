class Person:
    def greet(self):
        print("Hello!")

class Student(Person):
    def greet(self): 
        print("Hi, I am a student!")

person1 = Person()
student1 = Student()

person1.greet()
student1.greet()