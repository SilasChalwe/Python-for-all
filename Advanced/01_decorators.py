"""
01 - Decorators
================
This file covers:
  - What decorators are and how they work
  - Writing simple decorators
  - Preserving function metadata with @functools.wraps
  - Decorators with arguments (decorator factories)
  - Stacking multiple decorators
  - Class-based decorators
  - Built-in decorators: @property, @staticmethod, @classmethod
"""

import functools
import time
import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

# ==============================================================================
# 1. WHAT IS A DECORATOR?
# ==============================================================================
# A decorator is a function that takes another function as input,
# wraps it with additional behaviour, and returns the wrapped function.

print("=" * 45)
print("BASIC DECORATOR")
print("=" * 45)

def my_decorator(func):
    """A simple decorator that prints messages before/after the function."""
    @functools.wraps(func)   # preserves func's name, docstring, etc.
    def wrapper(*args, **kwargs):
        print(f"  Before calling '{func.__name__}'")
        result = func(*args, **kwargs)
        print(f"  After calling '{func.__name__}'")
        return result
    return wrapper

@my_decorator           # equivalent to: greet = my_decorator(greet)
def greet(name: str):
    """Greet someone."""
    print(f"  Hello, {name}!")

greet("Alice")
print(f"Function name preserved: {greet.__name__}")


# ==============================================================================
# 2. PRACTICAL DECORATOR: TIMER
# ==============================================================================

print("\n--- Timer Decorator ---")

def timer(func):
    """Measure how long a function takes to run."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start  = time.perf_counter()
        result = func(*args, **kwargs)
        end    = time.perf_counter()
        print(f"  ⏱  {func.__name__!r} took {end - start:.6f}s")
        return result
    return wrapper

@timer
def slow_sum(n: int) -> int:
    """Sum numbers 0 to n."""
    return sum(range(n))

slow_sum(1_000_000)


# ==============================================================================
# 3. DECORATOR WITH ARGUMENTS (DECORATOR FACTORY)
# ==============================================================================

print("\n--- Decorator with Arguments ---")

def repeat(times: int):
    """Decorator factory: repeat the function `times` times."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = None
            for _ in range(times):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

@repeat(3)
def say_hello(name: str):
    print(f"  Hello, {name}!")

say_hello("Bob")

# retry decorator
def retry(max_attempts: int = 3, exceptions: tuple = (Exception,)):
    """Retry a function up to max_attempts times on given exceptions."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_error = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_error = e
                    print(f"  Attempt {attempt} failed: {e}")
            raise last_error
        return wrapper
    return decorator

import random as _random
_random.seed(0)

@retry(max_attempts=4, exceptions=(ValueError,))
def flaky_function():
    """Fails randomly."""
    if _random.random() < 0.7:
        raise ValueError("Random failure!")
    return "Success!"

try:
    result = flaky_function()
    print(f"  Result: {result}")
except ValueError:
    print("  All attempts failed.")


# ==============================================================================
# 4. STACKING DECORATORS
# ==============================================================================

print("\n--- Stacking Decorators ---")

def bold(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return f"**{func(*args, **kwargs)}**"
    return wrapper

def uppercase(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs).upper()
    return wrapper

# Applied bottom-up: first uppercase, then bold
@bold
@uppercase
def say(text: str) -> str:
    return text

print(say("hello python"))   # **HELLO PYTHON**


# ==============================================================================
# 5. CLASS-BASED DECORATOR
# ==============================================================================

print("\n--- Class-Based Decorator ---")

class CallCounter:
    """Counts how many times the decorated function has been called."""

    def __init__(self, func):
        functools.update_wrapper(self, func)
        self.func  = func
        self.count = 0

    def __call__(self, *args, **kwargs):
        self.count += 1
        print(f"  Call #{self.count} to '{self.func.__name__}'")
        return self.func(*args, **kwargs)

@CallCounter
def add(a, b):
    return a + b

print(add(1, 2))
print(add(3, 4))
print(add(5, 6))
print(f"  Total calls: {add.count}")


# ==============================================================================
# 6. MEMOIZE DECORATOR (CACHING)
# ==============================================================================

print("\n--- Memoize Decorator ---")

def memoize(func):
    """Cache the results of a function based on its arguments."""
    cache = {}
    @functools.wraps(func)
    def wrapper(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]
    return wrapper

@memoize
def fib(n: int) -> int:
    if n <= 1:
        return n
    return fib(n - 1) + fib(n - 2)

print(f"fib(40) = {fib(40)}")
