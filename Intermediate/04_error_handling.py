"""
04 - Error Handling
====================
This file covers:
  - try / except / else / finally blocks
  - Catching specific exception types
  - The exception hierarchy
  - Raising exceptions with raise
  - Custom exception classes
  - The assert statement
  - Context managers for resource cleanup
"""

# ==============================================================================
# 1. BASIC try / except
# ==============================================================================

print("=" * 40)
print("BASIC TRY / EXCEPT")
print("=" * 40)

# Without error handling — this would crash:
# result = 10 / 0  # ZeroDivisionError

# With error handling:
try:
    result = 10 / 0
except ZeroDivisionError:
    print("Caught: Cannot divide by zero!")

# Catching multiple exception types
def safe_convert(value):
    """Try to convert value to an integer."""
    try:
        return int(value)
    except ValueError:
        print(f"  ValueError: '{value}' is not a valid integer.")
        return None
    except TypeError:
        print(f"  TypeError: Cannot convert {type(value).__name__} to int.")
        return None

print(safe_convert("42"))
print(safe_convert("hello"))
print(safe_convert(None))


# ==============================================================================
# 2. try / except / else / finally
# ==============================================================================

print("\n--- try / except / else / finally ---")

def read_file(filename):
    """
    Read a file safely.
    - else:    runs if no exception occurred
    - finally: ALWAYS runs (cleanup)
    """
    try:
        f = open(filename, "r")
    except FileNotFoundError:
        print(f"  File not found: {filename}")
        return None
    else:
        # This block runs only if no exception was raised
        content = f.read()
        f.close()
        print(f"  Successfully read {len(content)} characters.")
        return content
    finally:
        # This ALWAYS runs, even if an exception occurred
        print("  (finally block executed)")

read_file("/nonexistent/path.txt")


# ==============================================================================
# 3. COMMON EXCEPTION TYPES
# ==============================================================================

print("\n--- Common Exception Types ---")

exception_demos = [
    ("ZeroDivisionError",  lambda: 1 / 0),
    ("ValueError",         lambda: int("abc")),
    ("TypeError",          lambda: "2" + 2),
    ("IndexError",         lambda: [1,2,3][10]),
    ("KeyError",           lambda: {}["missing"]),
    ("AttributeError",     lambda: (42).upper()),
    ("NameError",          lambda: undefined_var),  # noqa
    ("OverflowError",      lambda: 10.0 ** 1000),
]

for name, func in exception_demos:
    try:
        func()
    except Exception as e:
        print(f"  {name}: {e}")


# ==============================================================================
# 4. CATCHING THE BASE EXCEPTION CLASS
# ==============================================================================

print("\n--- Catching Base Exception ---")

# Catch ALL exceptions (use sparingly — can hide bugs)
try:
    x = 1 / 0
except Exception as e:
    print(f"Caught generic exception: {type(e).__name__}: {e}")

# Best practice: catch the most specific exception you expect
# and let unexpected ones propagate


# ==============================================================================
# 5. RAISING EXCEPTIONS
# ==============================================================================

print("\n--- Raising Exceptions ---")

def set_age(age):
    """Set an age, validating it is a positive integer."""
    if not isinstance(age, int):
        raise TypeError(f"Age must be an int, got {type(age).__name__}")
    if age < 0 or age > 150:
        raise ValueError(f"Age must be between 0 and 150, got {age}")
    return age

try:
    set_age("twenty")
except TypeError as e:
    print(f"TypeError: {e}")

try:
    set_age(200)
except ValueError as e:
    print(f"ValueError: {e}")

print(f"Valid age: {set_age(25)}")

# Re-raising an exception
def risky():
    try:
        1 / 0
    except ZeroDivisionError:
        print("Logging the error...")
        raise   # re-raises the same exception

try:
    risky()
except ZeroDivisionError:
    print("Re-caught ZeroDivisionError in outer try.")


# ==============================================================================
# 6. CUSTOM EXCEPTIONS
# ==============================================================================

print("\n--- Custom Exceptions ---")

# Define custom exceptions by subclassing Exception
class InsufficientFundsError(Exception):
    """Raised when a bank account has insufficient funds."""
    def __init__(self, amount, balance):
        self.amount = amount
        self.balance = balance
        super().__init__(
            f"Cannot withdraw {amount}. Balance is only {balance}."
        )

class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        if amount > self.balance:
            raise InsufficientFundsError(amount, self.balance)
        self.balance -= amount
        return amount

account = BankAccount("Alice", balance=100)
account.deposit(50)
print(f"Balance after deposit: {account.balance}")

try:
    account.withdraw(200)
except InsufficientFundsError as e:
    print(f"Custom error: {e}")
    print(f"  Tried to withdraw: {e.amount}")
    print(f"  Current balance:   {e.balance}")


# ==============================================================================
# 7. assert STATEMENT
# ==============================================================================

print("\n--- assert Statement ---")

# assert is used for debugging and testing assumptions
# Raises AssertionError if condition is False

def divide(a, b):
    assert b != 0, "Divisor cannot be zero"
    return a / b

try:
    divide(10, 0)
except AssertionError as e:
    print(f"AssertionError: {e}")

print(divide(10, 2))

# NOTE: assertions can be disabled with 'python -O script.py'
# So don't use assert for input validation in production — use if/raise instead.
