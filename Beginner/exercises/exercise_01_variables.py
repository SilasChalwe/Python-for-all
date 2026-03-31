"""
Beginner Exercise 01 — Variables and Data Types
================================================
Complete each exercise below. Write your solution after each prompt.
Hints are provided if you get stuck.
"""

# ==============================================================================
# EXERCISE 1: Personal Info
# ==============================================================================
# Create variables to store your name (string), age (int), height in meters
# (float), and whether you are a student (bool). Then print all of them
# in a single formatted sentence.
#
# Expected output example:
#   Name: Alice | Age: 20 | Height: 1.70m | Student: True

# YOUR SOLUTION:


# ==============================================================================
# EXERCISE 2: Type Conversion
# ==============================================================================
# The variables below are all strings. Convert each one to its proper type,
# then compute and print the result of: price * quantity - discount
#
# Hint: use int() and float()

price_str    = "19.99"
quantity_str = "4"
discount_str = "5"

# YOUR SOLUTION:


# ==============================================================================
# EXERCISE 3: String Operations
# ==============================================================================
# Given the string below:
#   sentence = "  Hello, Python World!  "
# 1. Strip the whitespace from both ends
# 2. Convert it to uppercase
# 3. Replace "Python" with your name
# 4. Count how many letters 'l' appear in the final string
# 5. Print each result on its own line

sentence = "  Hello, Python World!  "

# YOUR SOLUTION:


# ==============================================================================
# EXERCISE 4: List and Dictionary Operations
# ==============================================================================
# You are given a list of scores and a student name.
# 1. Add a new score (77) to the end of the list
# 2. Remove the lowest score from the list
# 3. Calculate the average score
# 4. Store the name and average in a dictionary and print it
#
# Hint: use min(), sum(), len()

student_name = "Bob"
scores = [82, 67, 90, 55, 78]

# YOUR SOLUTION:


# ==============================================================================
# EXERCISE 5: FizzBuzz Variant
# ==============================================================================
# Create a list of numbers from 1 to 20.
# Build a new list where:
#   - multiples of 3 are replaced with "Fizz"
#   - multiples of 5 are replaced with "Buzz"
#   - multiples of both are replaced with "FizzBuzz"
#   - otherwise keep the number
# Print the resulting list.
#
# Hint: use a list comprehension or a for loop with conditionals

# YOUR SOLUTION:


# ==============================================================================
# SOLUTIONS (uncomment to check your work)
# ==============================================================================

# --- Exercise 1 ---
# name = "Alice"
# age = 20
# height = 1.70
# is_student = True
# print(f"Name: {name} | Age: {age} | Height: {height:.2f}m | Student: {is_student}")

# --- Exercise 2 ---
# price    = float(price_str)
# quantity = int(quantity_str)
# discount = float(discount_str)
# total = price * quantity - discount
# print(f"Total: {total:.2f}")

# --- Exercise 3 ---
# stripped  = sentence.strip()
# upper     = stripped.upper()
# replaced  = upper.replace("PYTHON", "SILAS")
# count_l   = replaced.count("L")
# print(stripped)
# print(upper)
# print(replaced)
# print("Count of 'L':", count_l)

# --- Exercise 4 ---
# scores.append(77)
# scores.remove(min(scores))
# average = sum(scores) / len(scores)
# student = {"name": student_name, "average": round(average, 2)}
# print(student)

# --- Exercise 5 ---
# result = [
#     "FizzBuzz" if n % 15 == 0 else "Fizz" if n % 3 == 0 else "Buzz" if n % 5 == 0 else n
#     for n in range(1, 21)
# ]
# print(result)
