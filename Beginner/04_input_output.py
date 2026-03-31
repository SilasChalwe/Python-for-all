"""
04 - Input and Output
======================
This file covers:
  - The print() function and its parameters
  - The input() function
  - Converting user input to other types
  - String formatting: f-strings, .format(), % formatting
  - Reading and displaying formatted data
"""

# ==============================================================================
# 1. THE print() FUNCTION
# ==============================================================================

print("=" * 40)
print("THE print() FUNCTION")
print("=" * 40)

# Basic printing
print("Hello, World!")
print(42)
print(3.14)
print(True)

# Printing multiple values (separated by a space by default)
print("Name:", "SilasChalwe", "Age:", 25)

# Changing the separator with sep=
print("2024", "01", "15", sep="-")    # 2024-01-15
print("one", "two", "three", sep=", ")

# Changing the end character with end= (default is newline '\n')
print("Loading", end="")
print("...", end=" ")
print("Done!")

# Printing nothing (just a blank line)
print()

# Printing a blank line between sections
print("Section 1")
print()
print("Section 2")


# ==============================================================================
# 2. STRING FORMATTING
# ==============================================================================

print("\n" + "=" * 40)
print("STRING FORMATTING")
print("=" * 40)

name = "SilasChalwe"
age = 25
score = 98.765

# --- f-strings (Python 3.6+, RECOMMENDED) ---
print(f"\nf-string: My name is {name} and I am {age} years old.")
print(f"Score: {score:.2f}")        # format to 2 decimal places
print(f"Score: {score:10.2f}")      # right-aligned in 10-char field
print(f"Name: {name:<15} |")        # left-align in 15-char field
print(f"Name: {name:>15} |")        # right-align
print(f"Name: {name:^15} |")        # center
print(f"Pi = {3.14159:.4f}")        # 4 decimal places
print(f"Hex: {255:#x}")             # hexadecimal with 0x prefix
print(f"Binary: {10:b}")            # binary representation
print(f"Thousands: {1_000_000:,}")  # comma separator

# --- .format() method ---
print("\n.format():")
print("My name is {} and I am {} years old.".format(name, age))
print("Score: {:.2f}".format(score))
print("{0} loves {1}. {1} is great.".format("SilasChalwe", "Python"))

# Named placeholders
print("{name} is {age} years old.".format(name=name, age=age))

# --- % formatting (older style, still encountered) ---
print("\n%% formatting:")
print("My name is %s and I am %d years old." % (name, age))
print("Score: %.2f" % score)


# ==============================================================================
# 3. THE input() FUNCTION
# ==============================================================================

print("\n" + "=" * 40)
print("THE input() FUNCTION")
print("=" * 40)

# NOTE: input() pauses execution and waits for user to press Enter.
# For demonstration, we will simulate with hardcoded values below.

# How to use input():
print("Example usage (not running interactively):")
print("  user_name = input('Enter your name: ')")
print("  user_age  = int(input('Enter your age: '))")

# Simulating input for demonstration purposes:
# Imagine the user typed "Alice" and "30"
simulated_name = "Alice"
simulated_age_str = "30"

# input() always returns a STRING — convert as needed
simulated_age = int(simulated_age_str)
print(f"\nSimulated name: {simulated_name} (type: {type(simulated_name).__name__})")
print(f"Simulated age:  {simulated_age}  (type: {type(simulated_age).__name__})")


# ==============================================================================
# 4. TYPE CONVERSION OF USER INPUT
# ==============================================================================

print("\n" + "=" * 40)
print("TYPE CONVERSION")
print("=" * 40)

# Always validate/convert input from users
raw_number = "42"        # as if from input()
raw_float  = "3.14"
raw_bool   = "True"

as_int   = int(raw_number)
as_float = float(raw_float)
as_bool  = raw_bool.strip().lower() == "true"   # manual bool conversion

print(f"int:   {as_int}   (type: {type(as_int).__name__})")
print(f"float: {as_float} (type: {type(as_float).__name__})")
print(f"bool:  {as_bool}  (type: {type(as_bool).__name__})")

# Safe conversion with error handling
def safe_int(value):
    """Convert to int, returning None on failure."""
    try:
        return int(value)
    except ValueError:
        return None

print(f"\nsafe_int('123')   = {safe_int('123')}")
print(f"safe_int('hello') = {safe_int('hello')}")


# ==============================================================================
# 5. PRACTICAL INPUT/OUTPUT EXAMPLES
# ==============================================================================

print("\n" + "=" * 40)
print("PRACTICAL EXAMPLES")
print("=" * 40)

# Receipt-style formatted output
def print_receipt(items):
    """Print a formatted receipt."""
    print("\n" + "=" * 30)
    print(f"{'RECEIPT':^30}")
    print("=" * 30)
    total = 0
    for item, price in items:
        print(f"{item:<20} ${price:>6.2f}")
        total += price
    print("-" * 30)
    print(f"{'TOTAL':<20} ${total:>6.2f}")
    print("=" * 30)

receipt_items = [
    ("Coffee", 3.50),
    ("Sandwich", 7.25),
    ("Water", 1.00),
    ("Dessert", 4.75),
]
print_receipt(receipt_items)
