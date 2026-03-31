"""
02 - Modules and Packages
==========================
This file covers:
  - Importing built-in modules
  - from...import syntax
  - Aliases with 'as'
  - The __name__ == "__main__" guard
  - Creating your own module (conceptual)
  - Exploring module contents with dir() and help()
"""

# ==============================================================================
# 1. IMPORTING MODULES
# ==============================================================================

# Import an entire module
import math
import random
import os

print("=" * 40)
print("IMPORTING MODULES")
print("=" * 40)

print("math.pi:", math.pi)
print("math.sqrt(16):", math.sqrt(16))
print("math.ceil(4.3):", math.ceil(4.3))
print("math.floor(4.9):", math.floor(4.9))


# ==============================================================================
# 2. FROM...IMPORT SYNTAX
# ==============================================================================

print("\n--- from...import ---")

# Import specific names from a module
from math import pi, sqrt, factorial
from random import randint, choice, shuffle

print(f"pi = {pi:.5f}")
print(f"sqrt(25) = {sqrt(25)}")
print(f"10! = {factorial(10)}")

print(f"Random int 1-10: {randint(1, 10)}")
colors = ["red", "green", "blue"]
print(f"Random choice: {choice(colors)}")
shuffle(colors)
print(f"Shuffled list: {colors}")


# ==============================================================================
# 3. ALIASES WITH 'as'
# ==============================================================================

print("\n--- Aliases ---")

import datetime as dt
import os.path as osp

now = dt.datetime.now()
print(f"Current datetime: {now.strftime('%Y-%m-%d %H:%M:%S')}")

home = os.path.expanduser("~")
print(f"Home directory exists: {osp.exists(home)}")

# The real power of aliases:
# import numpy as np      (convention)
# import pandas as pd     (convention)
# import matplotlib.pyplot as plt  (convention)


# ==============================================================================
# 4. EXPLORING MODULES
# ==============================================================================

print("\n--- Exploring Modules ---")

import string

# dir() lists all attributes/methods in a module
print("string module attributes (sample):")
public_attrs = [a for a in dir(string) if not a.startswith("_")]
print(public_attrs[:10])

# Useful string constants
print("\nstring.ascii_lowercase:", string.ascii_lowercase)
print("string.digits:", string.digits)
print("string.punctuation:", string.punctuation[:10], "...")


# ==============================================================================
# 5. STANDARD LIBRARY HIGHLIGHTS
# ==============================================================================

print("\n--- Standard Library Highlights ---")

# sys — system-specific parameters
import sys
print(f"Python version: {sys.version_info.major}.{sys.version_info.minor}")
print(f"Platform: {sys.platform}")

# os — operating system interface
print(f"\nCurrent directory: {os.getcwd()}")
print(f"PATH variable (first entry): {os.environ.get('PATH', '').split(os.pathsep)[0]}")

# pathlib — modern path handling (Python 3.4+)
from pathlib import Path
p = Path(".")
print(f"\nPath('.') absolute: {p.resolve()}")
print(f"Python files here: {list(p.glob('*.py'))[:3]}")


# ==============================================================================
# 6. __name__ == "__main__" GUARD
# ==============================================================================

# This pattern is crucial: code inside this block only runs when the file
# is executed directly, NOT when it is imported by another module.

def main():
    """Main function — entry point of the script."""
    print("\n--- __name__ guard ---")
    print(f"__name__ = {__name__}")
    print("This file is being run directly.")

if __name__ == "__main__":
    main()


# ==============================================================================
# 7. CREATING YOUR OWN MODULE (Conceptual)
# ==============================================================================

# To create a module, simply save a .py file with functions in it.
#
# Example: create a file called 'mymath.py':
#   def add(a, b):
#       return a + b
#
#   def square(n):
#       return n ** 2
#
# Then in another file:
#   import mymath
#   print(mymath.add(2, 3))
#
# To create a PACKAGE, create a folder with an __init__.py file inside it:
#   mypackage/
#       __init__.py
#       module1.py
#       module2.py
#
# Then import like:
#   from mypackage import module1
#   from mypackage.module2 import some_function
