"""
03 - Operators
===============
This file covers all Python operator types:
  - Arithmetic operators
  - Comparison operators
  - Logical operators
  - Assignment operators
  - Bitwise operators
  - Membership operators (in, not in)
  - Identity operators (is, is not)
"""

# ==============================================================================
# 1. ARITHMETIC OPERATORS
# ==============================================================================

print("=" * 40)
print("ARITHMETIC OPERATORS")
print("=" * 40)

a, b = 17, 5

print(f"a = {a}, b = {b}")
print(f"a + b  = {a + b}")   # Addition
print(f"a - b  = {a - b}")   # Subtraction
print(f"a * b  = {a * b}")   # Multiplication
print(f"a / b  = {a / b}")   # Division (always returns float)
print(f"a // b = {a // b}")  # Floor division (integer result)
print(f"a % b  = {a % b}")   # Modulo (remainder)
print(f"a ** b = {a ** b}")  # Exponentiation (17 to the power of 5)

# Useful tricks
print(f"\nIs a even? {a % 2 == 0}")
print(f"Is b even? {b % 2 == 0}")


# ==============================================================================
# 2. COMPARISON OPERATORS
# ==============================================================================

print("\n" + "=" * 40)
print("COMPARISON OPERATORS")
print("=" * 40)

x, y = 10, 20

print(f"x = {x}, y = {y}")
print(f"x == y  : {x == y}")   # Equal to
print(f"x != y  : {x != y}")   # Not equal to
print(f"x > y   : {x > y}")    # Greater than
print(f"x < y   : {x < y}")    # Less than
print(f"x >= y  : {x >= y}")   # Greater than or equal to
print(f"x <= y  : {x <= y}")   # Less than or equal to

# Chained comparisons (very Pythonic!)
age = 25
print(f"\nIs age between 18 and 65? {18 <= age <= 65}")


# ==============================================================================
# 3. LOGICAL OPERATORS
# ==============================================================================

print("\n" + "=" * 40)
print("LOGICAL OPERATORS")
print("=" * 40)

has_ticket = True
is_vip = False

# and — True only if BOTH are True
print(f"has_ticket and is_vip: {has_ticket and is_vip}")

# or — True if AT LEAST ONE is True
print(f"has_ticket or is_vip: {has_ticket or is_vip}")

# not — inverts the boolean value
print(f"not has_ticket: {not has_ticket}")
print(f"not is_vip:     {not is_vip}")

# Short-circuit evaluation
# 'and' stops at first False; 'or' stops at first True
print(f"\n0 and 'hello': {0 and 'hello'}")    # 0 (falsy, short-circuit)
print(f"1 and 'hello': {1 and 'hello'}")      # 'hello'
print(f"0 or 'hello':  {0 or 'hello'}")       # 'hello'
print(f"'' or 'default': {'' or 'default'}")  # 'default' (useful pattern!)


# ==============================================================================
# 4. ASSIGNMENT OPERATORS
# ==============================================================================

print("\n" + "=" * 40)
print("ASSIGNMENT OPERATORS")
print("=" * 40)

n = 10
print(f"Initial n = {n}")

n += 5;  print(f"n += 5  → {n}")   # n = n + 5
n -= 3;  print(f"n -= 3  → {n}")   # n = n - 3
n *= 2;  print(f"n *= 2  → {n}")   # n = n * 2
n //= 4; print(f"n //= 4 → {n}")   # n = n // 4
n **= 3; print(f"n **= 3 → {n}")   # n = n ** 3
n %= 7;  print(f"n %%= 7  → {n}")  # n = n % 7

# Walrus operator := (Python 3.8+) — assigns AND evaluates in one step
import re
data = "Hello World 42"
if match := re.search(r"\d+", data):
    print(f"\nWalrus operator: found number {match.group()}")


# ==============================================================================
# 5. BITWISE OPERATORS
# ==============================================================================

print("\n" + "=" * 40)
print("BITWISE OPERATORS")
print("=" * 40)

p, q = 0b1010, 0b1100  # binary literals: 10 and 12
print(f"p = {p} (binary: {bin(p)})")
print(f"q = {q} (binary: {bin(q)})")

print(f"p & q  = {p & q}  (AND:  {bin(p & q)})")   # bitwise AND
print(f"p | q  = {p | q}  (OR:   {bin(p | q)})")    # bitwise OR
print(f"p ^ q  = {p ^ q}  (XOR:  {bin(p ^ q)})")   # bitwise XOR
print(f"~p     = {~p}     (NOT:  {bin(~p)})")        # bitwise NOT
print(f"p << 1 = {p << 1} (LEFT SHIFT:  {bin(p << 1)})")  # multiply by 2
print(f"p >> 1 = {p >> 1} (RIGHT SHIFT: {bin(p >> 1)})")  # divide by 2


# ==============================================================================
# 6. MEMBERSHIP OPERATORS (in, not in)
# ==============================================================================

print("\n" + "=" * 40)
print("MEMBERSHIP OPERATORS")
print("=" * 40)

fruits = ["apple", "banana", "cherry"]
print(f"'apple' in fruits:     {'apple' in fruits}")
print(f"'mango' in fruits:     {'mango' in fruits}")
print(f"'mango' not in fruits: {'mango' not in fruits}")

# Works on strings too
text = "Python is great"
print(f"\n'Python' in text:  {'Python' in text}")
print(f"'Java' in text:    {'Java' in text}")

# Works on dictionaries (checks keys)
info = {"name": "Alice", "age": 30}
print(f"\n'name' in info: {'name' in info}")
print(f"'email' in info: {'email' in info}")


# ==============================================================================
# 7. IDENTITY OPERATORS (is, is not)
# ==============================================================================

print("\n" + "=" * 40)
print("IDENTITY OPERATORS")
print("=" * 40)

# 'is' checks if two variables point to the SAME object in memory
# '==' checks if the values are equal — these are different!

a = [1, 2, 3]
b = [1, 2, 3]
c = a   # c points to the same list as a

print(f"a == b:  {a == b}")   # True  (same values)
print(f"a is b:  {a is b}")   # False (different objects in memory)
print(f"a is c:  {a is c}")   # True  (same object)

# 'is' is commonly used to check for None
value = None
print(f"\nvalue is None:     {value is None}")
print(f"value is not None: {value is not None}")

# Small integers (-5 to 256) are cached by Python, so 'is' may return True
x = 100
y = 100
print(f"\nx is y (100): {x is y}")   # Usually True due to integer caching
