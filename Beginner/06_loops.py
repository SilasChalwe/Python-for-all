"""
06 - Loops
===========
This file covers:
  - for loops
  - while loops
  - range()
  - enumerate() and zip()
  - break, continue, pass
  - Nested loops
  - List, dict, and set comprehensions
"""

# ==============================================================================
# 1. for LOOPS
# ==============================================================================

print("=" * 40)
print("FOR LOOPS")
print("=" * 40)

# Looping over a list
fruits = ["apple", "banana", "cherry"]
for fruit in fruits:
    print(fruit)

# Looping over a string (character by character)
print()
for char in "Python":
    print(char, end=" ")
print()  # newline

# Looping over a dictionary
person = {"name": "Alice", "age": 30, "city": "Lusaka"}
print()
for key, value in person.items():
    print(f"{key}: {value}")


# ==============================================================================
# 2. range()
# ==============================================================================

print("\n" + "=" * 40)
print("range()")
print("=" * 40)

# range(stop)
print("range(5):", list(range(5)))          # 0 1 2 3 4

# range(start, stop)
print("range(2, 7):", list(range(2, 7)))    # 2 3 4 5 6

# range(start, stop, step)
print("range(0, 10, 2):", list(range(0, 10, 2)))   # even numbers
print("range(10, 0, -1):", list(range(10, 0, -1))) # countdown

# Common pattern: loop N times
for i in range(3):
    print(f"Iteration {i}")


# ==============================================================================
# 3. enumerate() AND zip()
# ==============================================================================

print("\n" + "=" * 40)
print("enumerate() AND zip()")
print("=" * 40)

# enumerate() — gives index AND value
languages = ["Python", "JavaScript", "Rust", "Go"]
print("enumerate():")
for index, lang in enumerate(languages, start=1):  # start=1 makes index 1-based
    print(f"  {index}. {lang}")

# zip() — iterate over multiple iterables at once
names = ["Alice", "Bob", "Charlie"]
scores = [95, 87, 72]
print("\nzip():")
for name, score in zip(names, scores):
    print(f"  {name}: {score}")

# zip creates pairs — stops at the shortest iterable
extra = [1, 2]
print("\nzip with different lengths:", list(zip(names, extra)))


# ==============================================================================
# 4. while LOOPS
# ==============================================================================

print("\n" + "=" * 40)
print("WHILE LOOPS")
print("=" * 40)

# Basic while loop
count = 0
while count < 5:
    print(f"count = {count}")
    count += 1  # ALWAYS update the condition variable to avoid infinite loops!

# while with else (else runs when condition becomes False normally)
n = 3
print()
while n > 0:
    print(f"n = {n}")
    n -= 1
else:
    print("Loop finished!")

# Using while True with a break
print("\nwhile True example:")
attempt = 0
while True:
    attempt += 1
    if attempt >= 3:
        print("Maximum attempts reached.")
        break
    print(f"Attempt {attempt}")


# ==============================================================================
# 5. break, continue, pass
# ==============================================================================

print("\n" + "=" * 40)
print("break, continue, pass")
print("=" * 40)

# break — exit the loop immediately
print("break example:")
for i in range(10):
    if i == 5:
        print(f"  Breaking at i={i}")
        break
    print(f"  i = {i}")

# continue — skip the rest of this iteration and go to next
print("\ncontinue example (skip even numbers):")
for i in range(10):
    if i % 2 == 0:
        continue   # skip even numbers
    print(f"  i = {i}")

# pass — do nothing (placeholder for empty blocks)
print("\npass example:")
for i in range(5):
    if i == 3:
        pass   # TODO: handle this case later
    else:
        print(f"  i = {i}")


# ==============================================================================
# 6. NESTED LOOPS
# ==============================================================================

print("\n" + "=" * 40)
print("NESTED LOOPS")
print("=" * 40)

# Multiplication table (3x3)
print("Multiplication table:")
for row in range(1, 4):
    for col in range(1, 4):
        print(f"{row * col:4}", end="")
    print()  # newline after each row

# Pattern printing
print("\nTriangle pattern:")
for i in range(1, 6):
    print("*" * i)


# ==============================================================================
# 7. LIST COMPREHENSIONS
# ==============================================================================

print("\n" + "=" * 40)
print("LIST COMPREHENSIONS")
print("=" * 40)

# Syntax: [expression for item in iterable if condition]

# Traditional way
squares_traditional = []
for x in range(1, 6):
    squares_traditional.append(x ** 2)

# Comprehension way (Pythonic!)
squares = [x ** 2 for x in range(1, 6)]
print("Squares:", squares)

# With a condition (filter)
even_squares = [x ** 2 for x in range(1, 11) if x % 2 == 0]
print("Even squares:", even_squares)

# Nested list comprehension (flatten a 2D list)
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flat = [num for row in matrix for num in row]
print("Flattened matrix:", flat)


# ==============================================================================
# 8. DICT AND SET COMPREHENSIONS
# ==============================================================================

print("\n" + "=" * 40)
print("DICT AND SET COMPREHENSIONS")
print("=" * 40)

# Dictionary comprehension
word_lengths = {word: len(word) for word in ["apple", "banana", "cherry"]}
print("Word lengths:", word_lengths)

# Set comprehension (no duplicates)
nums = [1, 2, 2, 3, 4, 4, 5]
unique_evens = {n for n in nums if n % 2 == 0}
print("Unique even numbers:", unique_evens)

# Generator expression (like list comprehension but lazy/memory-efficient)
total = sum(x ** 2 for x in range(1, 101))  # sum of squares 1..100
print("Sum of squares 1-100:", total)
