"""
02 - Generators
================
This file covers:
  - yield keyword
  - Generator functions vs regular functions
  - Generator expressions
  - The generator protocol (next(), StopIteration)
  - send(), throw(), close()
  - Chaining generators (yield from)
  - Practical use cases: infinite sequences, streaming, pipelines
"""

import itertools

# ==============================================================================
# 1. WHAT IS A GENERATOR?
# ==============================================================================
# A generator function uses 'yield' instead of 'return'.
# When called, it returns a generator object (lazy iterator) that produces
# values one at a time — values are NOT computed all at once.

print("=" * 45)
print("BASIC GENERATOR")
print("=" * 45)

def count_up(start, end):
    """Yield integers from start to end (inclusive)."""
    print(f"  [generator started: {start} to {end}]")
    for i in range(start, end + 1):
        print(f"  [about to yield {i}]")
        yield i
        print(f"  [resumed after yield {i}]")
    print("  [generator exhausted]")

gen = count_up(1, 3)
print(type(gen))         # <class 'generator'>

# next() retrieves the next value
print(next(gen))         # 1
print(next(gen))         # 2
print(next(gen))         # 3
# next(gen) would raise StopIteration

# Using in a for loop (recommended: handles StopIteration automatically)
print("\nUsing in for loop:")
for n in count_up(1, 3):
    print(f"  Got: {n}")


# ==============================================================================
# 2. GENERATOR EXPRESSIONS
# ==============================================================================

print("\n--- Generator Expressions ---")

# Syntax is like a list comprehension but with () instead of []
squares_list = [x**2 for x in range(1, 6)]     # list (all in memory)
squares_gen  = (x**2 for x in range(1, 6))      # generator (lazy)

print("List:", squares_list)
print("Generator object:", squares_gen)
print("Consumed:", list(squares_gen))

# Memory advantage: generator does not store all values
import sys
large_list = [x for x in range(1_000_000)]
large_gen  = (x for x in range(1_000_000))
print(f"\nList size:      {sys.getsizeof(large_list):>10,} bytes")
print(f"Generator size: {sys.getsizeof(large_gen):>10,} bytes")


# ==============================================================================
# 3. PRACTICAL GENERATORS
# ==============================================================================

print("\n--- Practical Generators ---")

# Infinite counter (safe because lazy — only computed on demand)
def infinite_counter(start=0, step=1):
    """Yield an infinite sequence of numbers."""
    n = start
    while True:
        yield n
        n += step

counter = infinite_counter(10, 5)
first_5 = [next(counter) for _ in range(5)]
print(f"Infinite counter (first 5): {first_5}")

# Fibonacci generator
def fibonacci():
    """Generate Fibonacci numbers indefinitely."""
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

fib = fibonacci()
fib_10 = [next(fib) for _ in range(10)]
print(f"Fibonacci (first 10): {fib_10}")

# Reading a large file line by line (memory efficient)
def read_large_file(filepath):
    """
    Generator that yields one line at a time from a file.
    Memory-efficient for very large files.
    """
    with open(filepath, "r") as f:
        for line in f:
            yield line.rstrip("\n")

# (Not running here since we don't have a large file, but the pattern is shown)
print("\nread_large_file() — lazy file reader defined (not run here).")


# ==============================================================================
# 4. yield from (DELEGATING TO A SUB-GENERATOR)
# ==============================================================================

print("\n--- yield from ---")

def chain(*iterables):
    """Yield from multiple iterables in sequence."""
    for it in iterables:
        yield from it   # delegates to sub-iterator

result = list(chain([1, 2], [3, 4], [5, 6]))
print(f"chain: {result}")

# Flattening nested structures with generators
def flatten(nested):
    """Recursively flatten a nested iterable."""
    for item in nested:
        if isinstance(item, (list, tuple)):
            yield from flatten(item)
        else:
            yield item

nested = [1, [2, 3, [4, 5]], 6, [7, [8, 9]]]
print(f"flatten: {list(flatten(nested))}")


# ==============================================================================
# 5. send(), throw(), close()
# ==============================================================================

print("\n--- send(), throw(), close() ---")

def accumulator():
    """
    A generator that maintains a running total.
    Use gen.send(value) to add a value; the generator yields the current total.
    """
    total = 0
    while True:
        value = yield total     # yield current total, then receive next value via send()
        if value is None:
            break
        total += value

acc = accumulator()
next(acc)              # prime the generator (advance to first yield)
print(acc.send(10))   # total = 10
print(acc.send(20))   # total = 30
print(acc.send(5))    # total = 35


# ==============================================================================
# 6. GENERATOR PIPELINE
# ==============================================================================

print("\n--- Generator Pipeline ---")

def integers(n):
    """Yield integers from 1 to n."""
    yield from range(1, n + 1)

def squared(nums):
    """Yield each number squared."""
    for n in nums:
        yield n ** 2

def only_even(nums):
    """Yield only even numbers."""
    for n in nums:
        if n % 2 == 0:
            yield n

# Chain generators into a pipeline — data flows lazily
pipeline = only_even(squared(integers(10)))
print(f"Pipeline (even squares 1-10): {list(pipeline)}")
