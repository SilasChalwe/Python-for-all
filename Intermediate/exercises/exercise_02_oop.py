"""
Intermediate Exercise 02 — Object-Oriented Programming
=========================================================
Practice OOP concepts: classes, inheritance, magic methods.
"""

# ==============================================================================
# EXERCISE 1: Library Book System
# ==============================================================================
# Create a Book class with attributes: title, author, year, isbn.
# Add methods:
#   - __str__: returns "Title by Author (Year)"
#   - is_new(): returns True if the book was published in the last 5 years
# Then create a Library class that:
#   - Holds a list of books
#   - add_book(book): add a book
#   - remove_book(isbn): remove by ISBN
#   - search(query): returns books where title or author contains query (case-insensitive)
#   - __len__: returns number of books

import datetime

# YOUR SOLUTION:


# ==============================================================================
# EXERCISE 2: Shape Hierarchy
# ==============================================================================
# Create a base class Shape with:
#   - A method area() that raises NotImplementedError
#   - A method perimeter() that raises NotImplementedError
#   - __str__ returning "ShapeName: area=X.XX, perimeter=X.XX"
#
# Create subclasses: Rectangle, Circle, Triangle
# Each must implement area() and perimeter().

import math

# YOUR SOLUTION:


# ==============================================================================
# EXERCISE 3: Bank Account
# ==============================================================================
# Create a BankAccount class:
#   - __init__(owner, balance=0)
#   - deposit(amount): add funds (must be positive)
#   - withdraw(amount): deduct funds (raise InsufficientFunds if not enough)
#   - transfer(amount, other_account): move money to another account
#   - __str__: "Account[owner]: $X.XX"
#   - history: keep a list of all transactions as strings

# YOUR SOLUTION:


# ==============================================================================
# EXERCISE 4: Inventory System
# ==============================================================================
# Create a Product class with: name, price, quantity
# Create an Inventory class that:
#   - Stores products by name in a dict
#   - add_product(product)
#   - sell(name, qty): reduce quantity; raise error if not enough stock
#   - restock(name, qty): increase quantity
#   - total_value: property returning sum of (price * quantity) for all products
#   - __iter__: allows looping over all products

# YOUR SOLUTION:


# ==============================================================================
# TESTS
# ==============================================================================

def test_library():
    print("Testing Library System...")
    book1 = Book("Python Crash Course", "Eric Matthes", 2019, "978-1593279288")
    book2 = Book("Clean Code", "Robert Martin", 2008, "978-0132350884")
    lib = Library()
    lib.add_book(book1)
    lib.add_book(book2)
    assert len(lib) == 2
    results = lib.search("python")
    assert len(results) == 1
    lib.remove_book("978-0132350884")
    assert len(lib) == 1
    print("  PASSED")

def test_shapes():
    print("Testing Shapes...")
    r = Rectangle(4, 5)
    assert abs(r.area() - 20) < 0.001
    assert abs(r.perimeter() - 18) < 0.001

    c = Circle(3)
    assert abs(c.area() - math.pi * 9) < 0.001
    assert abs(c.perimeter() - 2 * math.pi * 3) < 0.001
    print("  PASSED")

if __name__ == "__main__":
    # Uncomment after implementing:
    # test_library()
    # test_shapes()
    print("Implement the classes above, then uncomment the tests.")
