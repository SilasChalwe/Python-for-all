"""
05 - Advanced OOP
==================
This file covers:
  - Abstract Base Classes (ABC)
  - Mixins
  - Multiple inheritance and MRO (Method Resolution Order)
  - Descriptors (__get__, __set__, __delete__)
  - __slots__
  - Metaclasses
  - __getattr__ and __setattr__
"""

from abc import ABC, abstractmethod
import inspect

# ==============================================================================
# 1. ABSTRACT BASE CLASSES (ABC)
# ==============================================================================
# ABCs define an interface: subclasses MUST implement abstract methods.

print("=" * 45)
print("ABSTRACT BASE CLASSES")
print("=" * 45)

class Shape(ABC):
    """Abstract base class for geometric shapes."""

    @abstractmethod
    def area(self) -> float:
        """Return the area of the shape."""
        ...

    @abstractmethod
    def perimeter(self) -> float:
        """Return the perimeter of the shape."""
        ...

    def describe(self) -> str:
        """Concrete method available to all subclasses."""
        return (
            f"{self.__class__.__name__}: "
            f"area={self.area():.2f}, perimeter={self.perimeter():.2f}"
        )


class Circle(Shape):
    import math as _m
    def __init__(self, radius: float):
        self.radius = radius
    def area(self) -> float:
        import math
        return math.pi * self.radius ** 2
    def perimeter(self) -> float:
        import math
        return 2 * math.pi * self.radius

class Rectangle(Shape):
    def __init__(self, width: float, height: float):
        self.width = width
        self.height = height
    def area(self) -> float:
        return self.width * self.height
    def perimeter(self) -> float:
        return 2 * (self.width + self.height)

# Cannot instantiate Shape directly:
try:
    Shape()
except TypeError as e:
    print(f"Cannot instantiate ABC: {e}")

for shape in [Circle(5), Rectangle(4, 6)]:
    print(shape.describe())


# ==============================================================================
# 2. MIXINS
# ==============================================================================
# A Mixin is a class that provides methods to other classes via inheritance,
# but is NOT meant to stand alone.

print("\n--- Mixins ---")

class JsonMixin:
    """Mixin: adds JSON serialization to any class."""
    import json as _json

    def to_json(self) -> str:
        import json
        return json.dumps(self.__dict__, default=str, indent=2)

    @classmethod
    def from_json(cls, json_str: str):
        import json
        data = json.loads(json_str)
        obj = cls.__new__(cls)
        obj.__dict__.update(data)
        return obj


class ReprMixin:
    """Mixin: auto-generates __repr__ from instance attributes."""
    def __repr__(self) -> str:
        attrs = ", ".join(f"{k}={v!r}" for k, v in self.__dict__.items())
        return f"{self.__class__.__name__}({attrs})"


class EqualityMixin:
    """Mixin: equality based on __dict__ comparison."""
    def __eq__(self, other) -> bool:
        return type(self) is type(other) and self.__dict__ == other.__dict__
    def __hash__(self):
        return hash(tuple(sorted(self.__dict__.items())))


class Product(JsonMixin, ReprMixin, EqualityMixin):
    """A product that inherits from multiple mixins."""
    def __init__(self, name: str, price: float, stock: int):
        self.name  = name
        self.price = price
        self.stock = stock

p1 = Product("Widget", 9.99, 100)
p2 = Product("Widget", 9.99, 100)
print(repr(p1))
print(f"p1 == p2: {p1 == p2}")
print("JSON:", p1.to_json())


# ==============================================================================
# 3. MULTIPLE INHERITANCE AND MRO
# ==============================================================================

print("\n--- MRO ---")

class A:
    def hello(self): return "Hello from A"

class B(A):
    def hello(self): return "Hello from B"

class C(A):
    def hello(self): return "Hello from C"

class D(B, C):
    pass

d = D()
print(d.hello())              # B wins (C3 linearization)
print("MRO:", [cls.__name__ for cls in D.__mro__])


# ==============================================================================
# 4. DESCRIPTORS
# ==============================================================================
# A descriptor controls attribute access for a class.
# It defines __get__, __set__, __delete__.

print("\n--- Descriptors ---")

class TypedAttribute:
    """Descriptor that enforces a specific type for an attribute."""

    def __init__(self, name: str, expected_type: type):
        self._name = f"_{name}"
        self._type = expected_type

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return getattr(instance, self._name, None)

    def __set__(self, instance, value):
        if not isinstance(value, self._type):
            raise TypeError(
                f"Expected {self._type.__name__}, got {type(value).__name__}"
            )
        setattr(instance, self._name, value)

    def __delete__(self, instance):
        delattr(instance, self._name)


class Person:
    name = TypedAttribute("name", str)
    age  = TypedAttribute("age", int)

    def __init__(self, name: str, age: int):
        self.name = name
        self.age  = age

    def __repr__(self):
        return f"Person({self.name!r}, {self.age!r})"

p = Person("Alice", 30)
print(p)

try:
    p.age = "thirty"
except TypeError as e:
    print(f"TypeError: {e}")


# ==============================================================================
# 5. __slots__
# ==============================================================================
# __slots__ prevents __dict__ creation, reducing memory for many instances.

print("\n--- __slots__ ---")

class PointNoSlots:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class PointSlots:
    __slots__ = ("x", "y")   # only these attributes allowed
    def __init__(self, x, y):
        self.x = x
        self.y = y

import sys
p_no_slots  = PointNoSlots(1, 2)
p_slots     = PointSlots(1, 2)
print(f"Without __slots__: {sys.getsizeof(p_no_slots.__dict__)} bytes (dict)")
print(f"With __slots__:    no __dict__, memory saved")

# Cannot add new attributes with __slots__
try:
    p_slots.z = 3
except AttributeError as e:
    print(f"AttributeError: {e}")


# ==============================================================================
# 6. METACLASSES (BRIEF INTRODUCTION)
# ==============================================================================
# A metaclass is the class of a class — it controls class creation.

print("\n--- Metaclasses ---")

class SingletonMeta(type):
    """Metaclass that ensures only one instance of a class exists."""
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class Config(metaclass=SingletonMeta):
    """Application configuration — only one instance allowed."""
    def __init__(self):
        self.debug = False
        self.db_url = "sqlite:///app.db"

c1 = Config()
c2 = Config()
print(f"c1 is c2: {c1 is c2}")   # True — same instance
c1.debug = True
print(f"c2.debug (same object): {c2.debug}")
