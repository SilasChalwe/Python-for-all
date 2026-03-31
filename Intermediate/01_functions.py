"""
01 - Functions
===============
This file covers:
  - Defining and calling functions
  - Parameters: positional, keyword, default, *args, **kwargs
  - Return values (single and multiple)
  - Lambda functions
  - Docstrings
  - Type hints (annotations)
  - Scope: local vs global
  - Recursion
"""

from typing import Optional, Union


# ==============================================================================
# 1. DEFINING AND CALLING FUNCTIONS
# ==============================================================================

print("=" * 40)
print("BASIC FUNCTIONS")
print("=" * 40)

def greet():
    """Print a simple greeting."""
    print("Hello, World!")

def greet_name(name):
    """Greet a specific person."""
    print(f"Hello, {name}!")

greet()
greet_name("SilasChalwe")


# ==============================================================================
# 2. PARAMETERS AND RETURN VALUES
# ==============================================================================

print("\n--- Parameters & Return Values ---")

# Default parameter values
def power(base, exponent=2):
    """Return base raised to exponent. Default exponent is 2."""
    return base ** exponent

print(power(3))       # 9  (uses default exponent=2)
print(power(2, 10))   # 1024

# Keyword arguments — can be passed in any order
def describe_pet(name, animal="dog", age=1):
    """Describe a pet."""
    return f"{name} is a {age}-year-old {animal}."

print(describe_pet("Rex"))
print(describe_pet(animal="cat", name="Whiskers", age=3))

# Multiple return values (actually returns a tuple)
def min_max(numbers):
    """Return (minimum, maximum) of a list."""
    return min(numbers), max(numbers)

low, high = min_max([4, 7, 2, 9, 1])
print(f"min={low}, max={high}")


# ==============================================================================
# 3. *args AND **kwargs
# ==============================================================================

print("\n--- *args and **kwargs ---")

# *args — accepts any number of positional arguments as a tuple
def total(*args):
    """Sum all provided numbers."""
    return sum(args)

print(total(1, 2))
print(total(10, 20, 30, 40))

# **kwargs — accepts any number of keyword arguments as a dict
def display_info(**kwargs):
    """Print all keyword arguments."""
    for key, value in kwargs.items():
        print(f"  {key}: {value}")

display_info(name="Alice", age=30, city="Lusaka")

# Combining all parameter types
def mixed(required, default="hi", *args, **kwargs):
    """Demonstrate mixing parameter types."""
    print(f"required={required}, default={default}")
    print(f"  *args   = {args}")
    print(f"  **kwargs = {kwargs}")

mixed("must", "hello", 1, 2, 3, color="blue", size="large")

# Unpacking when calling a function
nums = [1, 2, 3]
opts = {"sep": ", ", "end": "!\n"}
print(*nums, **opts)   # prints: 1, 2, 3!


# ==============================================================================
# 4. LAMBDA FUNCTIONS
# ==============================================================================

print("\n--- Lambda Functions ---")

# Lambda: anonymous one-line function
square = lambda x: x ** 2
add    = lambda x, y: x + y

print(square(5))
print(add(3, 4))

# Common use: as a key in sort/sorted
words = ["banana", "fig", "apple", "cherry", "kiwi"]
words.sort(key=lambda w: len(w))   # sort by word length
print("By length:", words)

people = [("Alice", 30), ("Bob", 25), ("Charlie", 35)]
people.sort(key=lambda p: p[1])   # sort by age
print("By age:", people)

# With map() and filter()
numbers = [1, 2, 3, 4, 5, 6]
doubled = list(map(lambda x: x * 2, numbers))
evens   = list(filter(lambda x: x % 2 == 0, numbers))
print("Doubled:", doubled)
print("Evens:", evens)


# ==============================================================================
# 5. DOCSTRINGS
# ==============================================================================

print("\n--- Docstrings ---")

def calculate_area(width: float, height: float) -> float:
    """
    Calculate the area of a rectangle.

    Args:
        width  (float): The width of the rectangle.
        height (float): The height of the rectangle.

    Returns:
        float: The area (width * height).

    Raises:
        ValueError: If width or height is negative.

    Example:
        >>> calculate_area(5, 3)
        15.0
    """
    if width < 0 or height < 0:
        raise ValueError("Dimensions cannot be negative.")
    return float(width * height)

print(calculate_area(5, 3))
print(calculate_area.__doc__)


# ==============================================================================
# 6. TYPE HINTS (ANNOTATIONS)
# ==============================================================================

print("\n--- Type Hints ---")

# Type hints do not enforce types at runtime, but help editors and tools
def greet_user(name: str, times: int = 1) -> str:
    """Return a greeting string."""
    return f"Hello, {name}! " * times

def find_item(items: list, target: str) -> Optional[int]:
    """Return the index of target in items, or None if not found."""
    try:
        return items.index(target)
    except ValueError:
        return None

def process(value: Union[int, float]) -> str:
    """Accept int or float and return a description."""
    return f"Got number: {value}"

print(greet_user("Alice", 2))
print(find_item(["a", "b", "c"], "b"))
print(find_item(["a", "b", "c"], "z"))
print(process(42))


# ==============================================================================
# 7. SCOPE: LOCAL vs GLOBAL
# ==============================================================================

print("\n--- Scope ---")

global_var = "I am global"

def show_scope():
    local_var = "I am local"
    print(local_var)    # OK: local
    print(global_var)   # OK: reading global

def modify_global():
    global global_var   # declare intention to modify global
    global_var = "Modified global"

show_scope()
modify_global()
print(global_var)


# ==============================================================================
# 8. RECURSION
# ==============================================================================

print("\n--- Recursion ---")

def factorial(n: int) -> int:
    """Return n! (n factorial) using recursion."""
    if n <= 1:
        return 1
    return n * factorial(n - 1)   # function calls itself

def fibonacci(n: int) -> int:
    """Return the nth Fibonacci number."""
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

print("5! =", factorial(5))       # 120
print("Fib(10) =", fibonacci(10)) # 55

# Fibonacci with iteration (more efficient)
def fib_iter(n: int) -> int:
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a

print("Fib(10) iterative =", fib_iter(10))
