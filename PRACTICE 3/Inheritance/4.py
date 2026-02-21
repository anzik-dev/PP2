from abc import ABC, abstractmethod

class Animal(ABC):

    @abstractmethod
    def sound(self):
        pass

class Walker:
    def walk(self):
        print("Walking...")


class Dog(Animal, Walker):

    def sound(self):
        print("Woof!")

dog = Dog()
dog.sound()
dog.walk()