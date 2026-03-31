"""
Beginner Exercise 02 — Control Flow
=====================================
Practice conditionals and loops. Write your solution after each prompt.
"""

# ==============================================================================
# EXERCISE 1: Age Category
# ==============================================================================
# Given a person's age, print the appropriate category:
#   - 0-12:  "Child"
#   - 13-17: "Teenager"
#   - 18-64: "Adult"
#   - 65+:   "Senior"
# Test it with ages: 8, 15, 35, 70

ages_to_test = [8, 15, 35, 70]

# YOUR SOLUTION:


# ==============================================================================
# EXERCISE 2: Multiplication Table
# ==============================================================================
# Ask the user for a number (simulate with a variable) and print its
# multiplication table from 1 to 10.
# Example for number = 7:
#   7 x 1 = 7
#   7 x 2 = 14
#   ...
#   7 x 10 = 70

number = 7

# YOUR SOLUTION:


# ==============================================================================
# EXERCISE 3: Sum of Even Numbers
# ==============================================================================
# Using a loop and range(), calculate the sum of all even numbers
# from 1 to 100 (inclusive). Print the result.
# Expected answer: 2550

# YOUR SOLUTION:


# ==============================================================================
# EXERCISE 4: Find the Largest Number
# ==============================================================================
# Without using max(), write a loop that finds the largest number in the list.
# Print the largest value.

numbers = [34, 12, 78, 5, 90, 45, 23, 67]

# YOUR SOLUTION:


# ==============================================================================
# EXERCISE 5: Word Frequency Counter
# ==============================================================================
# Count how many times each word appears in the sentence below.
# Store the result in a dictionary and print it.
# Ignore case (treat "The" and "the" as the same word).
# Hint: use str.lower() and str.split()

sentence = "the cat sat on the mat the cat is fat"

# YOUR SOLUTION:


# ==============================================================================
# SOLUTIONS (uncomment to check your work)
# ==============================================================================

# --- Exercise 1 ---
# for age in ages_to_test:
#     if age <= 12:
#         category = "Child"
#     elif age <= 17:
#         category = "Teenager"
#     elif age <= 64:
#         category = "Adult"
#     else:
#         category = "Senior"
#     print(f"Age {age}: {category}")

# --- Exercise 2 ---
# for i in range(1, 11):
#     print(f"{number} x {i} = {number * i}")

# --- Exercise 3 ---
# total = sum(n for n in range(1, 101) if n % 2 == 0)
# print("Sum of even numbers 1-100:", total)

# --- Exercise 4 ---
# largest = numbers[0]
# for num in numbers[1:]:
#     if num > largest:
#         largest = num
# print("Largest:", largest)

# --- Exercise 5 ---
# freq = {}
# for word in sentence.lower().split():
#     freq[word] = freq.get(word, 0) + 1
# print(freq)
