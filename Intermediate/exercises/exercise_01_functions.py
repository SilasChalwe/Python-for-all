"""
Intermediate Exercise 01 — Functions
======================================
Practice writing and using functions. Solve each exercise independently.
"""

# ==============================================================================
# EXERCISE 1: Palindrome Checker
# ==============================================================================
# Write a function is_palindrome(text) that returns True if the text is a
# palindrome (reads the same forwards and backwards), ignoring spaces and case.
# Examples:
#   is_palindrome("racecar")       → True
#   is_palindrome("A man a plan a canal Panama") → True
#   is_palindrome("hello")         → False

# YOUR SOLUTION:
def is_palindrome(text: str) -> bool:
    pass


# ==============================================================================
# EXERCISE 2: Flatten Nested List
# ==============================================================================
# Write a function flatten(nested) that takes a list which may contain
# nested lists (of any depth) and returns a flat list.
# Example:
#   flatten([1, [2, 3], [4, [5, 6]], 7]) → [1, 2, 3, 4, 5, 6, 7]

# YOUR SOLUTION:
def flatten(nested):
    pass


# ==============================================================================
# EXERCISE 3: Caesar Cipher
# ==============================================================================
# Write a function caesar_cipher(text, shift) that shifts each letter in
# text by 'shift' positions (wrapping around the alphabet). Non-letters stay.
# Example:
#   caesar_cipher("Hello", 3) → "Khoor"
#   caesar_cipher("Khoor", -3) → "Hello"

# YOUR SOLUTION:
def caesar_cipher(text: str, shift: int) -> str:
    pass


# ==============================================================================
# EXERCISE 4: Statistics Functions
# ==============================================================================
# WITHOUT using the statistics module, write:
#   - mean(numbers)     → average of a list
#   - variance(numbers) → population variance
#   - std_dev(numbers)  → population standard deviation
# Use only math.sqrt from the math module.

import math

# YOUR SOLUTION:
def mean(numbers):
    pass

def variance(numbers):
    pass

def std_dev(numbers):
    pass


# ==============================================================================
# EXERCISE 5: Memoized Fibonacci
# ==============================================================================
# Write a fibonacci(n) function that uses a dictionary to cache results
# (memoization). It should be able to compute fib(100) instantly.

# YOUR SOLUTION:
def fibonacci(n: int, memo: dict = None) -> int:
    pass


# ==============================================================================
# TESTS — run to verify your solutions
# ==============================================================================

def run_tests():
    print("Testing Exercise 1: Palindrome")
    assert is_palindrome("racecar") == True
    assert is_palindrome("A man a plan a canal Panama") == True
    assert is_palindrome("hello") == False
    print("  PASSED")

    print("Testing Exercise 2: Flatten")
    assert flatten([1, [2, 3], [4, [5, 6]], 7]) == [1, 2, 3, 4, 5, 6, 7]
    assert flatten([]) == []
    print("  PASSED")

    print("Testing Exercise 3: Caesar Cipher")
    assert caesar_cipher("Hello", 3) == "Khoor"
    assert caesar_cipher("Khoor", -3) == "Hello"
    assert caesar_cipher("xyz", 3) == "abc"
    print("  PASSED")

    print("Testing Exercise 4: Statistics")
    data = [2, 4, 4, 4, 5, 5, 7, 9]
    assert abs(mean(data) - 5.0) < 0.001
    assert abs(variance(data) - 4.0) < 0.001
    assert abs(std_dev(data) - 2.0) < 0.001
    print("  PASSED")

    print("Testing Exercise 5: Fibonacci")
    assert fibonacci(10) == 55
    assert fibonacci(0) == 0
    assert fibonacci(1) == 1
    print("  PASSED")

    print("\nAll tests passed! 🎉")

if __name__ == "__main__":
    run_tests()


# ==============================================================================
# SOLUTIONS (uncomment to check)
# ==============================================================================

# def is_palindrome(text):
#     cleaned = "".join(c.lower() for c in text if c.isalnum())
#     return cleaned == cleaned[::-1]

# def flatten(nested):
#     result = []
#     for item in nested:
#         if isinstance(item, list):
#             result.extend(flatten(item))
#         else:
#             result.append(item)
#     return result

# def caesar_cipher(text, shift):
#     result = []
#     for char in text:
#         if char.isalpha():
#             base = ord('A') if char.isupper() else ord('a')
#             result.append(chr((ord(char) - base + shift) % 26 + base))
#         else:
#             result.append(char)
#     return "".join(result)

# def mean(numbers):
#     return sum(numbers) / len(numbers)
#
# def variance(numbers):
#     m = mean(numbers)
#     return sum((x - m) ** 2 for x in numbers) / len(numbers)
#
# def std_dev(numbers):
#     return math.sqrt(variance(numbers))

# def fibonacci(n, memo=None):
#     if memo is None:
#         memo = {}
#     if n in memo:
#         return memo[n]
#     if n <= 1:
#         return n
#     memo[n] = fibonacci(n - 1, memo) + fibonacci(n - 2, memo)
#     return memo[n]
