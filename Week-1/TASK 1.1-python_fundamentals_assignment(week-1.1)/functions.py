# functions_demo.py

# 1. Factorial function
def factorial(n):
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result

# 2. Fibonacci sequence function
def fibonacci(n):
    sequence = []
    a, b = 0, 1
    for _ in range(n):
        sequence.append(a)
        a, b = b, a + b
    return sequence

# 3. Prime check function
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

# 4. Palindrome check function
def is_palindrome(text):
    return text == text[::-1]

# --- Program Execution ---
num = int(input("Enter a number: "))
print(f"Factorial of {num} is {factorial(num)}")
print(f"First {num} Fibonacci numbers: {fibonacci(num)}")
print(f"Is {num} prime? {is_prime(num)}")

word = input("Enter a word: ")
print(f"Is '{word}' a palindrome? {is_palindrome(word)}")
