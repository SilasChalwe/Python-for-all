"""
05 - Conditionals
==================
This file covers:
  - if / elif / else statements
  - Nested conditionals
  - Ternary (conditional) expression
  - match-case statement (Python 3.10+)
  - Truthy and falsy values
"""

# ==============================================================================
# 1. if / elif / else
# ==============================================================================

print("=" * 40)
print("IF / ELIF / ELSE")
print("=" * 40)

# Basic if statement
temperature = 28

if temperature > 30:
    print("It's hot outside!")
elif temperature > 20:
    print("It's a nice day.")
elif temperature > 10:
    print("It's a bit chilly.")
else:
    print("It's cold!")

# Multiple conditions with and/or
age = 22
has_id = True

if age >= 18 and has_id:
    print("\nEntry allowed.")
else:
    print("\nEntry denied.")

# Grade classifier
score = 85

if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
elif score >= 70:
    grade = "C"
elif score >= 60:
    grade = "D"
else:
    grade = "F"

print(f"\nScore {score} → Grade: {grade}")


# ==============================================================================
# 2. NESTED CONDITIONALS
# ==============================================================================

print("\n" + "=" * 40)
print("NESTED CONDITIONALS")
print("=" * 40)

username = "admin"
password = "secret123"

if username == "admin":
    print("Username correct.")
    if password == "secret123":
        print("Password correct. Welcome, admin!")
    else:
        print("Wrong password.")
else:
    print("Unknown username.")


# ==============================================================================
# 3. TRUTHY AND FALSY VALUES
# ==============================================================================

print("\n" + "=" * 40)
print("TRUTHY AND FALSY VALUES")
print("=" * 40)

# These values are considered FALSY in Python:
falsy_values = [False, None, 0, 0.0, "", [], {}, set(), ()]

print("Falsy values:")
for val in falsy_values:
    print(f"  {repr(val):<12} → bool: {bool(val)}")

# Everything else is truthy
print("\nTruthy examples:")
truthy_values = [True, 1, -1, "hello", [0], {"key": 1}]
for val in truthy_values:
    print(f"  {repr(val):<15} → bool: {bool(val)}")

# Practical use: checking if a list is non-empty
items = []
if items:
    print("\nList has items.")
else:
    print("\nList is empty.")


# ==============================================================================
# 4. TERNARY (CONDITIONAL) EXPRESSION
# ==============================================================================

print("\n" + "=" * 40)
print("TERNARY EXPRESSION")
print("=" * 40)

# Syntax: value_if_true if condition else value_if_false
x = 10
result = "positive" if x > 0 else "non-positive"
print(f"x = {x} → {result}")

# Can be used inline
age = 20
status = "adult" if age >= 18 else "minor"
print(f"Age {age} → {status}")

# Nested ternary (use sparingly — can reduce readability)
score = 75
label = "pass" if score >= 60 else "fail"
print(f"Score {score} → {label}")


# ==============================================================================
# 5. match-case STATEMENT (Python 3.10+)
# ==============================================================================

print("\n" + "=" * 40)
print("MATCH-CASE (Python 3.10+)")
print("=" * 40)

# match-case is similar to switch-case in other languages but much more powerful
def describe_day(day):
    match day.lower():
        case "monday" | "tuesday" | "wednesday" | "thursday" | "friday":
            return "Weekday"
        case "saturday" | "sunday":
            return "Weekend"
        case _:                   # default case (like else)
            return "Unknown day"

for day in ["Monday", "Saturday", "Holiday"]:
    print(f"{day} → {describe_day(day)}")

# match on a value with guard clause (if condition)
def classify_score(score):
    match score:
        case s if s >= 90:
            return "A"
        case s if s >= 80:
            return "B"
        case s if s >= 70:
            return "C"
        case _:
            return "Below C"

print()
for s in [95, 83, 71, 55]:
    print(f"Score {s} → {classify_score(s)}")

# match on data structures (structural pattern matching)
def process_command(command):
    match command.split():
        case ["quit"]:
            return "Quitting..."
        case ["go", direction]:
            return f"Going {direction}"
        case ["pick", "up", item]:
            return f"Picked up {item}"
        case _:
            return "Unknown command"

print()
for cmd in ["quit", "go north", "pick up sword", "dance"]:
    print(f"'{cmd}' → {process_command(cmd)}")
