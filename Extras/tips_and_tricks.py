"""
Tips and Tricks
================
Useful Python tips, hidden gems, and performance tricks.
"""

# ==============================================================================
# 1. USEFUL BUILT-INS YOU MAY NOT KNOW
# ==============================================================================
print("--- Useful Built-ins ---")

# divmod — quotient and remainder at once
q, r = divmod(17, 5)
print(f"divmod(17,5) = {q} remainder {r}")

# abs, round, pow
print(abs(-42))
print(round(3.14159, 2))
print(pow(2, 10, 1000))  # (2**10) % 1000

# min/max with key
words = ["banana", "fig", "apple", "cherry"]
print("shortest:", min(words, key=len))
print("longest:", max(words, key=len))

# sorted with multiple keys
data = [("Alice", 30), ("Bob", 25), ("Alice", 25)]
print("sorted:", sorted(data, key=lambda x: (x[0], x[1])))

# vars(), dir(), type()
class Foo:
    x = 1
    y = 2

print("vars(Foo()):", vars(Foo()))

# zip_longest (fill missing values)
from itertools import zip_longest
a = [1, 2, 3]
b = ["a", "b"]
print("zip_longest:", list(zip_longest(a, b, fillvalue="?")))


# ==============================================================================
# 2. STRING TRICKS
# ==============================================================================
print("\n--- String Tricks ---")

# Repeat a string
print("ha" * 3)
print("-" * 30)

# Palindrome check
s = "racecar"
print(f"'{s}' is palindrome:", s == s[::-1])

# Count occurrences
text = "mississippi"
print("count 'ss':", text.count("ss"))

# Find and replace all
print("replace:", "hello world world".replace("world", "Python"))

# str.translate for char-level replacement
table = str.maketrans("aeiou", "AEIOU")
print("translate:", "hello world".translate(table))

# Check string content
print("isdigit:", "12345".isdigit())
print("isalpha:", "hello".isalpha())
print("isalnum:", "hello123".isalnum())


# ==============================================================================
# 3. LIST / DICT TRICKS
# ==============================================================================
print("\n--- List/Dict Tricks ---")

# Flatten a list
nested = [[1, 2], [3, 4], [5, 6]]
flat = [x for sub in nested for x in sub]
print("flat:", flat)

# Remove duplicates while preserving order
items = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3]
unique = list(dict.fromkeys(items))
print("unique ordered:", unique)

# Merge dicts (Python 3.9+)
d1 = {"a": 1, "b": 2}
d2 = {"b": 3, "c": 4}
merged = d1 | d2   # d2 values win on overlap
print("merged:", merged)

# Dict from two lists
keys   = ["name", "age", "city"]
values = ["Alice", 30, "Lusaka"]
d = dict(zip(keys, values))
print("dict from lists:", d)

# Invert a dict
inv = {v: k for k, v in d.items()}
print("inverted:", inv)

# Get nested value safely
config = {"db": {"host": "localhost"}}
host = config.get("db", {}).get("host", "unknown")
print("nested get:", host)


# ==============================================================================
# 4. PERFORMANCE TIPS
# ==============================================================================
print("\n--- Performance Tips ---")

import time

# Join strings with ''.join() — much faster than concatenation in a loop
n = 10_000

start = time.perf_counter()
s = ""
for _ in range(n):
    s += "x"
slow = time.perf_counter() - start

start = time.perf_counter()
s = "".join(["x"] * n)
fast = time.perf_counter() - start

print(f"String concat: {slow*1000:.3f}ms")
print(f"''.join():     {fast*1000:.3f}ms")
print(f"Speedup: ~{int(slow/fast+0.5)}x")

# Use sets for O(1) membership tests
big_list = list(range(100_000))
big_set  = set(big_list)

start = time.perf_counter()
_ = 99999 in big_list
list_time = time.perf_counter() - start

start = time.perf_counter()
_ = 99999 in big_set
set_time = time.perf_counter() - start

print(f"\nList membership: {list_time*1_000_000:.2f}µs")
print(f"Set membership:  {set_time*1_000_000:.2f}µs")


# ==============================================================================
# 5. ONE-LINERS
# ==============================================================================
print("\n--- One-liners ---")

# Fibonacci
fib = lambda n: n if n <= 1 else fib(n-1) + fib(n-2)
print("fib(10):", fib(10))

# Prime check
is_prime = lambda n: n > 1 and all(n % i for i in range(2, int(n**0.5)+1))
primes = [x for x in range(2, 30) if is_prime(x)]
print("Primes < 30:", primes)

# Flatten (any depth) using recursion
flatten = lambda lst: [x for item in lst for x in (flatten(item) if isinstance(item, list) else [item])]
print("flatten:", flatten([1, [2, [3, [4]]], 5]))

# Read a file as lines
# lines = open("file.txt").readlines()

# Most common element
from collections import Counter
most_common = lambda lst: Counter(lst).most_common(1)[0][0]
print("most common:", most_common([1, 2, 2, 3, 2, 1]))


# ==============================================================================
# 6. HIDDEN GEMS
# ==============================================================================
print("\n--- Hidden Gems ---")

# __all__ — controls what 'from module import *' exports
# __slots__ — reduces memory for many instances (see Advanced/05_advanced_oop.py)

# Chained comparison
x = 5
print("1 < x < 10:", 1 < x < 10)

# Underscore in numbers for readability
billion = 1_000_000_000
print(f"1 billion = {billion:,}")

# _ as throwaway variable
for _ in range(3):
    print("  tick", end=" ")
print()

# Unpacking with _
first, _, last = (1, 2, 3)
print(f"first={first}, last={last}")

# bool is a subclass of int
print("True + True =", True + True)    # 2
print("sum([True, False, True]):", sum([True, False, True]))  # 2 (count of True)
