"""
Pythonic Code
==============
Examples of idiomatic, Pythonic patterns that make your code cleaner
and more readable.
"""

# ==============================================================================
# 1. COMPREHENSIONS
# ==============================================================================
print("--- Comprehensions ---")

# List comprehension
squares = [x**2 for x in range(10) if x % 2 == 0]
print("Even squares:", squares)

# Dict comprehension
word_len = {w: len(w) for w in ["python", "is", "great"]}
print("Word lengths:", word_len)

# Set comprehension
unique_chars = {c.lower() for c in "Hello World" if c.isalpha()}
print("Unique chars:", sorted(unique_chars))

# Generator expression (lazy)
total = sum(x**2 for x in range(1000))
print("Sum of squares:", total)


# ==============================================================================
# 2. UNPACKING
# ==============================================================================
print("\n--- Unpacking ---")

# Tuple unpacking
a, b, c = 1, 2, 3
first, *rest = [1, 2, 3, 4, 5]
*init, last  = [1, 2, 3, 4, 5]
print(f"first={first}, rest={rest}, last={last}")

# Swap without temp variable
x, y = 10, 20
x, y = y, x
print(f"After swap: x={x}, y={y}")

# Unpacking in for loops
pairs = [(1, "one"), (2, "two"), (3, "three")]
for num, name in pairs:
    print(f"  {num}: {name}")


# ==============================================================================
# 3. PYTHONIC IDIOMS
# ==============================================================================
print("\n--- Pythonic Idioms ---")

# Use 'in' for membership tests
fruits = {"apple", "banana", "cherry"}
print("apple in fruits:", "apple" in fruits)

# Use enumerate() instead of range(len(...))
items = ["a", "b", "c"]
for i, item in enumerate(items, start=1):
    print(f"  {i}. {item}")

# Use zip() to iterate pairs
names  = ["Alice", "Bob", "Charlie"]
scores = [90, 85, 92]
for name, score in zip(names, scores):
    print(f"  {name}: {score}")

# Conditional expression (ternary)
age = 20
label = "adult" if age >= 18 else "minor"
print("Label:", label)

# any() and all()
nums = [2, 4, 6, 8]
print("All even:", all(n % 2 == 0 for n in nums))
print("Any > 5:", any(n > 5 for n in nums))

# Get with default
config = {"debug": True}
port = config.get("port", 8080)
print("Port:", port)

# Walrus operator (Python 3.8+)
data = [1, 2, 3, 4, 5]
if (n := len(data)) > 3:
    print(f"List is long: {n} items")

# String joining (not concatenation in a loop)
words = ["Hello", "World", "from", "Python"]
sentence = " ".join(words)
print(sentence)

# Truthiness checks
empty_list = []
if not empty_list:
    print("List is empty")

value = None
result = value or "default"
print("Result:", result)


# ==============================================================================
# 4. FUNCTIONAL TOOLS
# ==============================================================================
print("\n--- Functional Tools ---")

from functools import reduce

numbers = [1, 2, 3, 4, 5]
print("map (x2):", list(map(lambda x: x * 2, numbers)))
print("filter (>3):", list(filter(lambda x: x > 3, numbers)))
print("reduce (sum):", reduce(lambda a, b: a + b, numbers))

# sorted with key
people = [("Alice", 30), ("Bob", 25), ("Charlie", 35)]
by_age = sorted(people, key=lambda p: p[1])
print("By age:", by_age)
