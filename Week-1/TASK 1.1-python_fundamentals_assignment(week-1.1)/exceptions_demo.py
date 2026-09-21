# exceptions.py
try:
    num = int(input("Enter a number: "))
    result = 10 / num
    print("Result:", result)
except ValueError:
    print("Please enter a valid number.")
except ZeroDivisionError:
    print("Division by zero is not allowed.")
finally:
    print("Program completed.")
