"""
Best Practices
===============
Python coding best practices, conventions, and patterns.
"""

# ==============================================================================
# 1. NAMING CONVENTIONS (PEP 8)
# ==============================================================================

# Variables and functions: snake_case
user_name = "Alice"
def calculate_average(numbers): pass

# Classes: PascalCase
class UserAccount: pass

# Constants: UPPER_SNAKE_CASE
MAX_RETRY_COUNT = 3
DEFAULT_TIMEOUT = 30

# Private: leading underscore
_internal_helper = "not for external use"

# "Dunder" (special): double underscores
# __init__, __str__, __repr__, etc.


# ==============================================================================
# 2. DOCSTRINGS
# ==============================================================================

def divide(a: float, b: float) -> float:
    """
    Divide a by b.

    Args:
        a (float): Numerator.
        b (float): Denominator (must not be zero).

    Returns:
        float: The result of a / b.

    Raises:
        ValueError: If b is zero.

    Example:
        >>> divide(10, 2)
        5.0
    """
    if b == 0:
        raise ValueError("Cannot divide by zero.")
    return a / b


# ==============================================================================
# 3. TYPE HINTS
# ==============================================================================

from typing import Optional, Union, List, Dict

def greet(name: str, times: int = 1) -> str:
    return ("Hello, " + name + "! ") * times

def find(items: List[str], target: str) -> Optional[int]:
    try:
        return items.index(target)
    except ValueError:
        return None


# ==============================================================================
# 4. ERROR HANDLING
# ==============================================================================

# Be specific with exception types
def read_config(path: str) -> dict:
    import json
    try:
        with open(path) as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Config file not found: {path}")
        return {}
    except json.JSONDecodeError as e:
        print(f"Invalid JSON: {e}")
        return {}
    # Let unexpected exceptions propagate


# ==============================================================================
# 5. DRY PRINCIPLE (Don't Repeat Yourself)
# ==============================================================================

# BAD: repeated logic
def area_circle_bad(r): return 3.14159 * r * r
def circumference_bad(r): return 2 * 3.14159 * r

# GOOD: single source of truth
import math
PI = math.pi
def area_circle(r: float) -> float:     return PI * r**2
def circumference(r: float) -> float:   return 2 * PI * r


# ==============================================================================
# 6. PREFER CONTEXT MANAGERS FOR RESOURCES
# ==============================================================================

# BAD: file may not be closed on error
# f = open("file.txt")
# data = f.read()
# f.close()

# GOOD: always closed, even on exception
# with open("file.txt") as f:
#     data = f.read()


# ==============================================================================
# 7. USE LOGGING INSTEAD OF PRINT IN PRODUCTION
# ==============================================================================

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def process(data):
    logger.info("Processing %d items", len(data))
    # logger.debug("Data: %s", data)   # only shown in DEBUG mode
    # logger.warning("Something odd")
    # logger.error("Something failed")
    return data

process([1, 2, 3])


# ==============================================================================
# 8. SMALL, FOCUSED FUNCTIONS
# ==============================================================================

# BAD: function doing too many things
def bad_process(filepath):
    with open(filepath) as f: lines = f.readlines()
    data = [l.strip().split(",") for l in lines if l.strip()]
    result = []
    for row in data:
        if len(row) >= 2:
            result.append({"name": row[0], "score": int(row[1])})
    result.sort(key=lambda x: x["score"], reverse=True)
    with open("output.txt", "w") as f:
        for r in result: f.write(f"{r['name']}: {r['score']}\n")
    return result

# GOOD: split into small, single-responsibility functions
def read_lines(filepath):
    with open(filepath) as f:
        return [l.strip() for l in f if l.strip()]

def parse_row(row_str: str) -> dict:
    parts = row_str.split(",")
    return {"name": parts[0].strip(), "score": int(parts[1].strip())}

def sort_by_score(records: list) -> list:
    return sorted(records, key=lambda r: r["score"], reverse=True)


print("Best practices module loaded.")
