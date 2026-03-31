"""
Mini Project — Simple Calculator
==================================
A command-line calculator that performs basic arithmetic operations.

Skills used: functions, loops, conditionals, input/output, error handling
"""


def add(a, b):
    """Return the sum of a and b."""
    return a + b


def subtract(a, b):
    """Return the difference of a and b."""
    return a - b


def multiply(a, b):
    """Return the product of a and b."""
    return a * b


def divide(a, b):
    """Return the quotient of a and b. Raises ValueError for division by zero."""
    if b == 0:
        raise ValueError("Cannot divide by zero!")
    return a / b


def get_number(prompt):
    """Prompt the user for a number and return it as a float."""
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("  Invalid input. Please enter a number.")


def calculator():
    """Run the interactive calculator."""
    print("=" * 35)
    print("       🧮  CALCULATOR")
    print("=" * 35)

    operations = {
        "1": ("+", add),
        "2": ("-", subtract),
        "3": ("*", multiply),
        "4": ("/", divide),
    }

    while True:
        print("\nSelect an operation:")
        print("  1. Addition       (+)")
        print("  2. Subtraction    (-)")
        print("  3. Multiplication (*)")
        print("  4. Division       (/)")
        print("  5. Exit")

        choice = input("\nEnter choice (1-5): ").strip()

        if choice == "5":
            print("Goodbye! 👋")
            break

        if choice not in operations:
            print("Invalid choice. Please select 1-5.")
            continue

        symbol, operation = operations[choice]

        num1 = get_number("Enter first number:  ")
        num2 = get_number("Enter second number: ")

        try:
            result = operation(num1, num2)
            print(f"\n  {num1} {symbol} {num2} = {result}")
        except ValueError as e:
            print(f"  Error: {e}")


if __name__ == "__main__":
    calculator()
