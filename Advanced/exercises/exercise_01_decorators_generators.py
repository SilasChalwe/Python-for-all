"""
Advanced Exercise 01 — Decorators and Generators
==================================================
Practice advanced Python concepts. Implement each function/class.
"""

import time
import functools

# ==============================================================================
# EXERCISE 1: Logging Decorator
# ==============================================================================
# Write a decorator 'log_calls' that:
#   - Prints the function name, arguments, and keyword arguments before calling
#   - Prints the return value after calling
#   - Prints how long it took (in ms)
# Use @functools.wraps to preserve the original function's metadata.
#
# Example output:
#   Calling 'add' with args=(1, 2), kwargs={}
#   'add' returned 3 in 0.01ms

def log_calls(func):
    pass  # YOUR SOLUTION


# ==============================================================================
# EXERCISE 2: Validate Arguments Decorator
# ==============================================================================
# Write a decorator factory 'validate_types' that accepts type annotations
# and raises TypeError if any argument doesn't match.
#
# Usage:
#   @validate_types(str, int)
#   def repeat(text, times):
#       return text * times
#
#   repeat("hi", 3)     → "hihihi"
#   repeat("hi", "3")   → TypeError

def validate_types(*types):
    pass  # YOUR SOLUTION


# ==============================================================================
# EXERCISE 3: Infinite Range Generator
# ==============================================================================
# Write a generator function 'infinite_range(start, step)' that generates
# an infinite sequence starting at 'start', incrementing by 'step'.
#
# Also write 'take(n, iterable)' that returns the first n items from any iterable.
#
# Example:
#   list(take(5, infinite_range(0, 2)))  → [0, 2, 4, 6, 8]
#   list(take(5, infinite_range(10, -3))) → [10, 7, 4, 1, -2]

def infinite_range(start=0, step=1):
    pass  # YOUR SOLUTION

def take(n, iterable):
    pass  # YOUR SOLUTION


# ==============================================================================
# EXERCISE 4: Running Statistics Generator
# ==============================================================================
# Write a generator-based coroutine 'running_stats()' that accepts numbers
# via send() and yields (count, mean, min, max) after each value.
#
# Usage:
#   gen = running_stats()
#   next(gen)         # prime the generator
#   gen.send(10)  → (1, 10.0, 10, 10)
#   gen.send(20)  → (2, 15.0, 10, 20)
#   gen.send(5)   → (3, 11.67, 5, 20)

def running_stats():
    pass  # YOUR SOLUTION


# ==============================================================================
# EXERCISE 5: Lazy File Line Reader
# ==============================================================================
# Write a generator 'grep_lines(filepath, pattern)' that:
#   - Opens a file
#   - Yields (line_number, line) for each line containing 'pattern' (case-insensitive)
# This should be memory-efficient (do not read the entire file at once).

import re
import tempfile, os

def grep_lines(filepath: str, pattern: str):
    pass  # YOUR SOLUTION


# ==============================================================================
# TESTS
# ==============================================================================

def test_log_calls():
    @log_calls
    def multiply(a, b):
        return a * b
    result = multiply(3, 4)
    assert result == 12
    print("  Exercise 1 (log_calls): PASSED")

def test_validate_types():
    @validate_types(str, int)
    def repeat(text, times):
        return text * times
    assert repeat("hi", 3) == "hihihi"
    try:
        repeat("hi", "3")
        assert False, "Should have raised TypeError"
    except TypeError:
        pass
    print("  Exercise 2 (validate_types): PASSED")

def test_infinite_range():
    assert list(take(5, infinite_range(0, 2)))   == [0, 2, 4, 6, 8]
    assert list(take(3, infinite_range(10, -3))) == [10, 7, 4]
    print("  Exercise 3 (infinite_range): PASSED")

def test_running_stats():
    gen = running_stats()
    next(gen)
    r1 = gen.send(10)
    r2 = gen.send(20)
    r3 = gen.send(5)
    assert r1 == (1, 10.0, 10, 10)
    assert r2 == (2, 15.0, 10, 20)
    assert r3[0] == 3 and abs(r3[1] - 35/3) < 0.01 and r3[2] == 5 and r3[3] == 20
    print("  Exercise 4 (running_stats): PASSED")

def test_grep_lines():
    tmpfile = tempfile.mktemp(suffix=".txt")
    with open(tmpfile, "w") as f:
        f.write("Hello World\nPython is great\nhello again\nJava too\n")
    results = list(grep_lines(tmpfile, "hello"))
    os.unlink(tmpfile)
    assert len(results) == 2
    assert results[0][0] == 1  # line 1
    assert results[1][0] == 3  # line 3
    print("  Exercise 5 (grep_lines): PASSED")

if __name__ == "__main__":
    print("Running tests...")
    # Uncomment after implementing:
    # test_log_calls()
    # test_validate_types()
    # test_infinite_range()
    # test_running_stats()
    # test_grep_lines()
    print("\nImplement the functions above, then uncomment the tests.")
