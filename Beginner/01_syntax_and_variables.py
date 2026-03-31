"""
01 - Python Syntax and Variables
=================================
This file covers:
  - Basic Python syntax rules
  - Variables and assignment
  - Naming conventions
  - Built-in data types overview
  - The type() function
  - Multiple assignment
  - Constants
"""

# ==============================================================================
# 1. PYTHON SYNTAX BASICS
# ==============================================================================

# Python uses indentation (spaces/tabs) to define code blocks — no curly braces!
# Lines do NOT end with semicolons (though you can use them, it's not Pythonic).

# This is a single-line comment

"""
This is a multi-line string often used as a docstring or block comment.
It does not get executed.
"""

# Printing to the console
print("Hello, World!")   # The classic first program
print("Python is fun!")


# ==============================================================================
# 2. VARIABLES AND ASSIGNMENT
# ==============================================================================

# Variables are created when you assign a value — no declaration needed.
name = "SilasChalwe"       # str (string)
age = 25                   # int (integer)
height = 1.75              # float (floating-point number)
is_student = True          # bool (boolean)
nothing = None             # NoneType — represents the absence of a value

print("\n--- Variables ---")
print("Name:", name)
print("Age:", age)
print("Height:", height)
print("Is student:", is_student)
print("Nothing:", nothing)


# ==============================================================================
# 3. TYPE CHECKING WITH type()
# ==============================================================================

print("\n--- Types ---")
print(type(name))        # <class 'str'>
print(type(age))         # <class 'int'>
print(type(height))      # <class 'float'>
print(type(is_student))  # <class 'bool'>
print(type(nothing))     # <class 'NoneType'>


# ==============================================================================
# 4. VARIABLE NAMING RULES
# ==============================================================================

# VALID variable names:
my_variable = 1       # snake_case is the Python convention
_private = 3          # leading underscore = convention for "private"
variable1 = 4         # letters and digits are fine (not at the start)

# INVALID (would cause SyntaxError):
# 1variable = 5       # cannot start with a digit
# my-var = 6          # hyphens are not allowed
# class = 7           # 'class' is a reserved keyword

# Python keywords (cannot be used as variable names):
import keyword
print("\nPython reserved keywords:")
print(keyword.kwlist)


# ==============================================================================
# 5. MULTIPLE ASSIGNMENT
# ==============================================================================

# Assign the same value to multiple variables at once
x = y = z = 0
print("\nx, y, z:", x, y, z)

# Unpack values into multiple variables simultaneously
a, b, c = 10, 20, 30
print("a, b, c:", a, b, c)

# Swap two variables without a temporary variable (Pythonic!)
a, b = b, a
print("After swap — a:", a, ", b:", b)

# Extended unpacking with *
first, *rest = [1, 2, 3, 4, 5]
print("first:", first, "  rest:", rest)


# ==============================================================================
# 6. TYPE CONVERSION (CASTING)
# ==============================================================================

print("\n--- Type Conversion ---")

num_str = "42"
num_int = int(num_str)      # str -> int
num_float = float(num_str)  # str -> float
back_to_str = str(num_int)  # int -> str

print(type(num_int), num_int)
print(type(num_float), num_float)
print(type(back_to_str), back_to_str)

# Be careful with invalid conversions:
# int("hello")  # ValueError!


# ==============================================================================
# 7. CONSTANTS (CONVENTION)
# ==============================================================================

# Python has no built-in constant type — use ALL_CAPS as a convention
PI = 3.14159
MAX_CONNECTIONS = 100
DEFAULT_NAME = "Guest"

print("\n--- Constants ---")
print("PI =", PI)
print("MAX_CONNECTIONS =", MAX_CONNECTIONS)


# ==============================================================================
# 8. DYNAMIC TYPING
# ==============================================================================

# Python is dynamically typed — a variable can change its type
dynamic = 10
print("\ndynamic:", dynamic, type(dynamic))

dynamic = "now I'm a string"
print("dynamic:", dynamic, type(dynamic))

dynamic = [1, 2, 3]
print("dynamic:", dynamic, type(dynamic))
