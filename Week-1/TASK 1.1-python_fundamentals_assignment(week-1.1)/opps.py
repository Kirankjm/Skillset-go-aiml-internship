# oop_simple.py

# Base class
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def introduce(self):
        print(f"My name is {self.name}, I am {self.age} years old.")


# Student class (inherits from Person)
class Student(Person):
    def __init__(self, name, age, roll, marks):
        super().__init__(name, age)
        self.roll = roll
        self.marks = marks

    def show_details(self):
        print(f"Roll: {self.roll}, Marks: {self.marks}")


# Teacher class (inherits from Person)
class Teacher(Person):
    def __init__(self, name, age, subject):
        super().__init__(name, age)
        self.subject = subject

    def show_subject(self):
        print(f"I teach {self.subject}.")


# --- Program Execution ---
student1 = Student("karim", 23, 204, 88)
teacher1 = Teacher("Anita", 35, "Computer Science")

student1.introduce()
student1.show_details()

print("\n")

teacher1.introduce()
teacher1.show_subject()
