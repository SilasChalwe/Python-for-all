"""
02 - Data Types
================
This file covers Python's core built-in data types:
  - Strings (str)
  - Lists (list)
  - Tuples (tuple)
  - Sets (set)
  - Dictionaries (dict)
"""

# ==============================================================================
# 1. STRINGS (str)
# ==============================================================================

print("=" * 40)
print("STRINGS")
print("=" * 40)

# Creating strings
single = 'Hello'
double = "World"
multi  = """This is a
multi-line string."""

print(single, double)
print(multi)

# String length
name = "SilasChalwe"
print("\nLength:", len(name))

# Indexing (0-based; negative indexing counts from the end)
print("First char:", name[0])    # S
print("Last char:", name[-1])    # e

# Slicing [start:stop:step]
print("Slice [0:5]:", name[0:5])   # Silas
print("Reverse:", name[::-1])       # ewlahCsaliS

# Common string methods
sentence = "  python is awesome  "
print("\nUpper:", sentence.upper())
print("Lower:", sentence.lower())
print("Strip:", sentence.strip())
print("Replace:", sentence.replace("awesome", "great"))
print("Split:", sentence.strip().split(" "))
print("Starts with 'python':", sentence.strip().startswith("python"))

# String formatting
language = "Python"
version = 3.11

# f-strings (recommended, Python 3.6+)
print(f"\nf-string: {language} version {version}")

# .format() method
print("format(): {} version {}".format(language, version))

# % formatting (older style)
print("%% style: %s version %.1f" % (language, version))

# Checking membership
print("\n'is' in sentence:", "is" in sentence)

# String is immutable — you cannot do name[0] = 'X'


# ==============================================================================
# 2. LISTS (list)
# ==============================================================================

print("\n" + "=" * 40)
print("LISTS")
print("=" * 40)

# Lists are ordered, mutable, and allow duplicates
fruits = ["apple", "banana", "cherry", "apple"]
numbers = [1, 2, 3, 4, 5]
mixed = [1, "two", 3.0, True, None]  # lists can hold different types

print("Fruits:", fruits)
print("Numbers:", numbers)
print("Mixed:", mixed)

# Indexing and slicing (same as strings)
print("\nFirst fruit:", fruits[0])
print("Last fruit:", fruits[-1])
print("Slice [1:3]:", fruits[1:3])

# Modifying lists
fruits.append("mango")       # add to end
fruits.insert(1, "orange")   # insert at index
fruits.remove("apple")       # remove first occurrence
popped = fruits.pop()        # remove and return last item
print("\nAfter modifications:", fruits)
print("Popped:", popped)

# Other useful list methods
numbers.sort()
numbers.reverse()
print("\nSorted & reversed:", numbers)
print("Count of 1:", numbers.count(1))
print("Index of 3:", numbers.index(3))

# Nested lists (2D list)
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
print("\nMatrix row 1:", matrix[0])
print("Element [1][2]:", matrix[1][2])  # 6


# ==============================================================================
# 3. TUPLES (tuple)
# ==============================================================================

print("\n" + "=" * 40)
print("TUPLES")
print("=" * 40)

# Tuples are ordered, IMMUTABLE, and allow duplicates
coordinates = (10.5, 20.3)
rgb = (255, 128, 0)
single_tuple = (42,)   # trailing comma required for single-element tuple

print("Coordinates:", coordinates)
print("RGB:", rgb)
print("Single:", single_tuple)

# Tuple unpacking
x, y = coordinates
print("x =", x, ", y =", y)

# Convert between tuple and list
as_list = list(rgb)
as_tuple = tuple(as_list)
print("As list:", as_list)
print("As tuple:", as_tuple)


# ==============================================================================
# 4. SETS (set)
# ==============================================================================

print("\n" + "=" * 40)
print("SETS")
print("=" * 40)

# Sets are unordered, mutable, and do NOT allow duplicates
unique_nums = {1, 2, 3, 4, 4, 5, 5}  # duplicates are removed automatically
print("Set:", unique_nums)

# Adding and removing elements
unique_nums.add(6)
unique_nums.discard(1)   # discard does not raise error if element not found
print("After add/discard:", unique_nums)

# Set operations
a = {1, 2, 3, 4}
b = {3, 4, 5, 6}

print("\nUnion (|):", a | b)
print("Intersection (&):", a & b)
print("Difference (-):", a - b)
print("Symmetric difference (^):", a ^ b)

# Membership check (very fast in sets)
print("\n3 in a:", 3 in a)
print("7 in a:", 7 in a)


# ==============================================================================
# 5. DICTIONARIES (dict)
# ==============================================================================

print("\n" + "=" * 40)
print("DICTIONARIES")
print("=" * 40)

# Dictionaries store key-value pairs; ordered (Python 3.7+) and mutable
person = {
    "name": "SilasChalwe",
    "age": 25,
    "language": "Python",
    "active": True
}

print("Person:", person)

# Accessing values
print("\nName:", person["name"])
print("Age (get):", person.get("age"))
print("Missing key (get):", person.get("email", "Not found"))

# Adding and updating
person["email"] = "silas@example.com"
person["age"] = 26
print("\nUpdated person:", person)

# Removing entries
removed = person.pop("active")
print("Removed 'active':", removed)

# Iterating over a dictionary
print("\nKey-Value pairs:")
for key, value in person.items():
    print(f"  {key}: {value}")

# Dictionary comprehension
squares = {n: n**2 for n in range(1, 6)}
print("\nSquares dict:", squares)

# Nested dictionary
employee = {
    "id": 101,
    "info": {
        "name": "Alice",
        "role": "Developer"
    }
}
print("Nested access:", employee["info"]["name"])
