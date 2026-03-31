"""
05 - Object-Oriented Programming (OOP) Basics
==============================================
This file covers:
  - Classes and objects
  - __init__ constructor
  - Instance methods and class variables
  - Inheritance and super()
  - Method overriding
  - Magic methods: __str__, __repr__, __len__, __eq__
  - Properties with @property
  - Static methods and class methods
"""

# ==============================================================================
# 1. DEFINING A CLASS
# ==============================================================================

print("=" * 40)
print("DEFINING A CLASS")
print("=" * 40)

class Dog:
    """Represents a dog."""

    # Class variable — shared by ALL instances
    species = "Canis familiaris"

    def __init__(self, name: str, breed: str, age: int):
        """Initialize a Dog instance."""
        # Instance variables — unique to each object
        self.name  = name
        self.breed = breed
        self.age   = age

    def bark(self) -> str:
        """Return the dog's bark."""
        return f"{self.name} says: Woof!"

    def description(self) -> str:
        """Return a description of the dog."""
        return f"{self.name} is a {self.age}-year-old {self.breed}."

    # Magic method: string representation for users
    def __str__(self) -> str:
        return f"Dog(name={self.name}, breed={self.breed})"

    # Magic method: string representation for developers/debugging
    def __repr__(self) -> str:
        return f"Dog({self.name!r}, {self.breed!r}, {self.age!r})"

# Creating instances
dog1 = Dog("Rex",    "German Shepherd", 3)
dog2 = Dog("Buddy",  "Labrador",        5)

print(dog1.description())
print(dog2.bark())
print(f"Species: {Dog.species}")   # accessing class variable
print(str(dog1))
print(repr(dog2))


# ==============================================================================
# 2. INHERITANCE
# ==============================================================================

print("\n" + "=" * 40)
print("INHERITANCE")
print("=" * 40)

class Animal:
    """Base class for all animals."""

    def __init__(self, name: str, sound: str):
        self.name  = name
        self.sound = sound

    def speak(self) -> str:
        return f"{self.name} says {self.sound}!"

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.name!r})"


class Cat(Animal):
    """A Cat — inherits from Animal."""

    def __init__(self, name: str, indoor: bool = True):
        super().__init__(name, "Meow")  # call the parent __init__
        self.indoor = indoor

    def purr(self) -> str:
        return f"{self.name} purrs..."


class GuideDog(Dog):
    """A GuideDog — inherits from Dog."""

    def __init__(self, name: str, breed: str, age: int, handler: str):
        super().__init__(name, breed, age)
        self.handler = handler

    # Override the parent method
    def description(self) -> str:
        base = super().description()   # call parent's description()
        return f"{base} Handler: {self.handler}."


cat = Cat("Whiskers")
guide = GuideDog("Buddy", "Labrador", 4, "John")

print(cat.speak())
print(cat.purr())
print(guide.description())

# isinstance() and issubclass()
print(f"\ncat is Animal: {isinstance(cat, Animal)}")
print(f"GuideDog is Dog: {issubclass(GuideDog, Dog)}")


# ==============================================================================
# 3. MAGIC (DUNDER) METHODS
# ==============================================================================

print("\n" + "=" * 40)
print("MAGIC METHODS")
print("=" * 40)

class Vector:
    """2D vector with operator overloading."""

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __str__(self)  -> str: return f"Vector({self.x}, {self.y})"
    def __repr__(self) -> str: return f"Vector({self.x!r}, {self.y!r})"

    def __add__(self, other):  return Vector(self.x + other.x, self.y + other.y)
    def __sub__(self, other):  return Vector(self.x - other.x, self.y - other.y)
    def __mul__(self, scalar): return Vector(self.x * scalar, self.y * scalar)

    def __eq__(self, other) -> bool:
        return self.x == other.x and self.y == other.y

    def __len__(self) -> int:
        """Return the squared magnitude (as int for demo)."""
        return int(self.x**2 + self.y**2)

    def magnitude(self) -> float:
        return (self.x**2 + self.y**2) ** 0.5


v1 = Vector(3, 4)
v2 = Vector(1, 2)
print(v1)
print(v1 + v2)
print(v1 - v2)
print(v1 * 3)
print(f"Equal: {v1 == v2}")
print(f"Magnitude of v1: {v1.magnitude()}")


# ==============================================================================
# 4. PROPERTIES
# ==============================================================================

print("\n" + "=" * 40)
print("PROPERTIES")
print("=" * 40)

class Circle:
    """A circle with radius validation."""

    def __init__(self, radius: float):
        self._radius = radius   # convention: leading _ means "private"

    @property
    def radius(self) -> float:
        """Get the radius."""
        return self._radius

    @radius.setter
    def radius(self, value: float):
        """Set the radius — must be positive."""
        if value < 0:
            raise ValueError("Radius cannot be negative.")
        self._radius = value

    @property
    def area(self) -> float:
        """Computed property — no setter needed."""
        import math
        return math.pi * self._radius ** 2

    @property
    def circumference(self) -> float:
        import math
        return 2 * math.pi * self._radius


c = Circle(5)
print(f"Radius: {c.radius}")
print(f"Area: {c.area:.2f}")
print(f"Circumference: {c.circumference:.2f}")

c.radius = 10   # uses setter
print(f"New radius: {c.radius}")

try:
    c.radius = -1
except ValueError as e:
    print(f"Error: {e}")


# ==============================================================================
# 5. CLASS METHODS AND STATIC METHODS
# ==============================================================================

print("\n" + "=" * 40)
print("CLASS AND STATIC METHODS")
print("=" * 40)

class Date:
    """Represents a date with alternative constructors."""

    def __init__(self, year: int, month: int, day: int):
        self.year  = year
        self.month = month
        self.day   = day

    @classmethod
    def from_string(cls, date_str: str):
        """Alternative constructor: create from 'YYYY-MM-DD' string."""
        year, month, day = map(int, date_str.split("-"))
        return cls(year, month, day)

    @classmethod
    def today(cls):
        """Create a Date from today's date."""
        import datetime
        d = datetime.date.today()
        return cls(d.year, d.month, d.day)

    @staticmethod
    def is_leap_year(year: int) -> bool:
        """Check if a year is a leap year (no instance or class needed)."""
        return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

    def __str__(self) -> str:
        return f"{self.year}-{self.month:02d}-{self.day:02d}"


d1 = Date(2024, 3, 15)
d2 = Date.from_string("2025-07-04")
d3 = Date.today()

print(f"d1: {d1}")
print(f"d2: {d2}")
print(f"Today: {d3}")
print(f"2024 is leap year: {Date.is_leap_year(2024)}")
print(f"2023 is leap year: {Date.is_leap_year(2023)}")
