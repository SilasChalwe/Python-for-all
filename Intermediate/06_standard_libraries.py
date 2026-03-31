"""
06 - Standard Libraries
========================
This file showcases useful modules from the Python standard library:
  - os, sys
  - math, statistics
  - random
  - datetime
  - collections (Counter, defaultdict, deque, namedtuple)
  - itertools
  - functools
  - re (regular expressions)
"""

# ==============================================================================
# 1. os and sys
# ==============================================================================

import os, sys

print("=" * 40)
print("os AND sys")
print("=" * 40)

print(f"CWD: {os.getcwd()}")
print(f"Python executable: {sys.executable}")
print(f"Python version: {sys.version_info[:3]}")
print(f"Platform: {sys.platform}")
print(f"HOME env var: {os.environ.get('HOME', 'N/A')}")

# os.path
path = "/home/user/documents/report.pdf"
print(f"\nDirname:  {os.path.dirname(path)}")
print(f"Basename: {os.path.basename(path)}")
print(f"Splitext: {os.path.splitext(path)}")


# ==============================================================================
# 2. math AND statistics
# ==============================================================================

import math
import statistics

print("\n" + "=" * 40)
print("math AND statistics")
print("=" * 40)

print(f"pi:        {math.pi:.6f}")
print(f"e:         {math.e:.6f}")
print(f"sqrt(144): {math.sqrt(144)}")
print(f"log2(8):   {math.log2(8)}")
print(f"log10(100):{math.log10(100)}")
print(f"ceil(4.1): {math.ceil(4.1)}")
print(f"floor(4.9):{math.floor(4.9)}")
print(f"gcd(12,8): {math.gcd(12, 8)}")
print(f"comb(5,2): {math.comb(5, 2)}")  # combinations: C(5,2) = 10

data = [10, 20, 30, 40, 50, 55, 60]
print(f"\nmean:    {statistics.mean(data)}")
print(f"median:  {statistics.median(data)}")
print(f"stdev:   {statistics.stdev(data):.2f}")
print(f"variance:{statistics.variance(data):.2f}")


# ==============================================================================
# 3. random
# ==============================================================================

import random

print("\n" + "=" * 40)
print("random")
print("=" * 40)

random.seed(42)   # seed for reproducibility
print(f"randint(1,10):   {random.randint(1, 10)}")
print(f"random():        {random.random():.4f}")      # float [0.0, 1.0)
print(f"uniform(1, 5):   {random.uniform(1, 5):.4f}")

items = ["a", "b", "c", "d", "e"]
print(f"choice:    {random.choice(items)}")
print(f"choices(3):{random.choices(items, k=3)}")

sample = random.sample(range(100), 5)   # 5 unique random numbers
print(f"sample(5): {sample}")

random.shuffle(items)
print(f"shuffled:  {items}")


# ==============================================================================
# 4. datetime
# ==============================================================================

import datetime

print("\n" + "=" * 40)
print("datetime")
print("=" * 40)

now    = datetime.datetime.now()
today  = datetime.date.today()
utcnow = datetime.datetime.utcnow()

print(f"Now:    {now}")
print(f"Today:  {today}")
print(f"UTC:    {utcnow}")
print(f"Year:   {now.year}, Month: {now.month}, Day: {now.day}")
print(f"Formatted: {now.strftime('%B %d, %Y at %H:%M')}")

# Date arithmetic with timedelta
tomorrow   = today + datetime.timedelta(days=1)
last_week  = today - datetime.timedelta(weeks=1)
print(f"\nTomorrow:  {tomorrow}")
print(f"Last week: {last_week}")

# Parsing a date string
birth_str = "1999-07-15"
birth_date = datetime.datetime.strptime(birth_str, "%Y-%m-%d").date()
age_days = (today - birth_date).days
print(f"\nBirth: {birth_date}, Days lived: {age_days}")


# ==============================================================================
# 5. collections
# ==============================================================================

from collections import Counter, defaultdict, deque, namedtuple

print("\n" + "=" * 40)
print("collections")
print("=" * 40)

# Counter — count elements
words = "the quick brown fox jumps over the lazy dog the fox".split()
counter = Counter(words)
print(f"Counter: {counter}")
print(f"Most common 3: {counter.most_common(3)}")

# defaultdict — dict with a default factory (no KeyError)
dd = defaultdict(list)
for name, score in [("Alice", 90), ("Bob", 85), ("Alice", 95)]:
    dd[name].append(score)
print(f"\ndefaultdict: {dict(dd)}")

# deque — double-ended queue (fast append/pop from both ends)
dq = deque([1, 2, 3])
dq.appendleft(0)    # fast left append
dq.append(4)        # fast right append
dq.popleft()        # fast left pop
print(f"\ndeque: {list(dq)}")
print(f"deque maxlen example: {deque(range(10), maxlen=3)}")  # keeps last 3

# namedtuple — tuple with named fields
Point   = namedtuple("Point", ["x", "y"])
Person  = namedtuple("Person", ["name", "age", "city"])

pt = Point(3, 4)
p  = Person("Alice", 30, "Lusaka")
print(f"\nPoint: {pt}, x={pt.x}, y={pt.y}")
print(f"Person: {p}, name={p.name}")


# ==============================================================================
# 6. itertools
# ==============================================================================

import itertools

print("\n" + "=" * 40)
print("itertools")
print("=" * 40)

# chain — combine multiple iterables
combined = list(itertools.chain([1, 2], [3, 4], [5, 6]))
print(f"chain: {combined}")

# product — cartesian product
suits  = ["♠", "♥"]
values = ["A", "K"]
cards  = list(itertools.product(suits, values))
print(f"product: {cards}")

# combinations and permutations
items = ["A", "B", "C"]
print(f"combinations(2):  {list(itertools.combinations(items, 2))}")
print(f"permutations(2):  {list(itertools.permutations(items, 2))}")

# groupby — group consecutive equal elements
data = [1, 1, 2, 3, 3, 3, 4]
grouped = {key: list(vals) for key, vals in itertools.groupby(data)}
print(f"groupby: {grouped}")

# islice — slice an iterator
print(f"islice(range(100), 5): {list(itertools.islice(range(100), 5))}")


# ==============================================================================
# 7. functools
# ==============================================================================

import functools

print("\n" + "=" * 40)
print("functools")
print("=" * 40)

# reduce — reduce list to single value
total = functools.reduce(lambda acc, x: acc + x, [1, 2, 3, 4, 5])
print(f"reduce (sum): {total}")

# partial — create a new function with pre-filled arguments
def multiply(a, b):
    return a * b

double = functools.partial(multiply, b=2)
triple = functools.partial(multiply, b=3)
print(f"double(5): {double(5)}")
print(f"triple(5): {triple(5)}")

# lru_cache — memoize function results (great for recursive functions)
@functools.lru_cache(maxsize=128)
def fib(n: int) -> int:
    if n <= 1:
        return n
    return fib(n - 1) + fib(n - 2)

print(f"fib(35): {fib(35)}")  # fast due to caching
print(f"Cache info: {fib.cache_info()}")
