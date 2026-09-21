
# Print multiplication table of 8
for i in range(1, 11):
    print(f"8 x {i} = {8 * i}")
print("\n")

# 2. While loop - Countdown from 5
print("Countdown (while loop):")
count = 5
while count > 0:
    print(count)
    count -= 1
print("Blast off!")

print("\n")

# 3. Nested loop - Pattern printing
print("Pattern (nested for loop):")
for row in range(1, 6):
    for col in range(row):
        print("*", end=" ")
    print()

print("\n")

# 4. Loop with break and continue
print("Loop with break and continue:")
for i in range(1, 10):
    if i == 5:
        print("Skipping 5 (continue)")
        continue
    if i == 8:
        print("Breaking at 8")
        break
    print(i)
