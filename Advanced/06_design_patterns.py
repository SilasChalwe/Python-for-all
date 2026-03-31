"""
06 - Design Patterns in Python
================================
This file demonstrates common software design patterns implemented in Python:
  - Singleton
  - Factory Method
  - Observer (Event System)
  - Strategy
  - Command
  - Decorator (the design pattern, not the Python decorator syntax)
"""

from abc import ABC, abstractmethod
from typing import Callable, List

# ==============================================================================
# 1. SINGLETON PATTERN
# ==============================================================================
# Ensures a class has only one instance.

print("=" * 45)
print("1. SINGLETON")
print("=" * 45)

class DatabaseConnection:
    """Singleton: only one database connection at a time."""
    _instance = None

    def __new__(cls, url: str = "sqlite:///app.db"):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.url = url
            cls._instance.connected = False
            print(f"  Created new DB connection to {url}")
        return cls._instance

    def connect(self):
        self.connected = True
        print(f"  Connected to {self.url}")

    def disconnect(self):
        self.connected = False


db1 = DatabaseConnection()
db2 = DatabaseConnection("postgres://other")   # same instance, url doesn't change!
db1.connect()
print(f"  db1 is db2: {db1 is db2}")
print(f"  db2.url: {db2.url}")   # same as db1's url


# ==============================================================================
# 2. FACTORY METHOD PATTERN
# ==============================================================================
# Defines an interface for creating objects but lets subclasses decide which
# class to instantiate.

print("\n" + "=" * 45)
print("2. FACTORY METHOD")
print("=" * 45)

class Notification(ABC):
    @abstractmethod
    def send(self, message: str) -> str:
        ...

class EmailNotification(Notification):
    def __init__(self, address: str):
        self.address = address
    def send(self, message: str) -> str:
        return f"Email to {self.address}: {message}"

class SMSNotification(Notification):
    def __init__(self, phone: str):
        self.phone = phone
    def send(self, message: str) -> str:
        return f"SMS to {self.phone}: {message}"

class PushNotification(Notification):
    def __init__(self, token: str):
        self.token = token
    def send(self, message: str) -> str:
        return f"Push [{self.token}]: {message}"

class NotificationFactory:
    """Factory that creates Notification objects based on a type string."""
    _registry = {
        "email": EmailNotification,
        "sms":   SMSNotification,
        "push":  PushNotification,
    }

    @classmethod
    def create(cls, notif_type: str, **kwargs) -> Notification:
        klass = cls._registry.get(notif_type.lower())
        if not klass:
            raise ValueError(f"Unknown notification type: {notif_type}")
        return klass(**kwargs)

    @classmethod
    def register(cls, name: str, klass):
        """Allow registering new notification types."""
        cls._registry[name] = klass

email = NotificationFactory.create("email", address="user@example.com")
sms   = NotificationFactory.create("sms", phone="+260971234567")
push  = NotificationFactory.create("push", token="abc123")

for n in [email, sms, push]:
    print(f"  {n.send('Hello!')}")


# ==============================================================================
# 3. OBSERVER PATTERN (EVENT SYSTEM)
# ==============================================================================
# Defines a one-to-many dependency: when one object changes, all dependents
# are notified automatically.

print("\n" + "=" * 45)
print("3. OBSERVER")
print("=" * 45)

class EventEmitter:
    """Observable: emits named events to registered listeners."""

    def __init__(self):
        self._listeners: dict[str, List[Callable]] = {}

    def on(self, event: str, listener: Callable):
        """Register a listener for an event."""
        self._listeners.setdefault(event, []).append(listener)
        return self  # allows chaining: emitter.on("a", fn1).on("b", fn2)

    def off(self, event: str, listener: Callable):
        """Unregister a listener."""
        if event in self._listeners:
            self._listeners[event].remove(listener)

    def emit(self, event: str, *args, **kwargs):
        """Trigger all listeners for an event."""
        for listener in self._listeners.get(event, []):
            listener(*args, **kwargs)


class StockMarket(EventEmitter):
    def __init__(self, symbol: str, price: float):
        super().__init__()
        self.symbol = symbol
        self._price = price

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, new_price: float):
        old_price = self._price
        self._price = new_price
        change = new_price - old_price
        self.emit("price_change", symbol=self.symbol,
                  old=old_price, new=new_price, change=change)

def price_logger(symbol, old, new, change):
    direction = "📈" if change > 0 else "📉"
    print(f"  {direction} {symbol}: ${old:.2f} → ${new:.2f} ({change:+.2f})")

def alert_big_move(symbol, old, new, change):
    if abs(change) > 5:
        print(f"  ⚠️  ALERT: {symbol} moved more than $5!")

stock = StockMarket("PYTH", 100.0)
stock.on("price_change", price_logger)
stock.on("price_change", alert_big_move)

stock.price = 103.5
stock.price = 95.0    # triggers alert!
stock.price = 96.0


# ==============================================================================
# 4. STRATEGY PATTERN
# ==============================================================================
# Defines a family of algorithms, encapsulates each one, and makes them
# interchangeable at runtime.

print("\n" + "=" * 45)
print("4. STRATEGY")
print("=" * 45)

class SortStrategy(ABC):
    @abstractmethod
    def sort(self, data: list) -> list:
        ...

class BubbleSortStrategy(SortStrategy):
    def sort(self, data: list) -> list:
        arr = data[:]
        for i in range(len(arr)):
            for j in range(len(arr) - i - 1):
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
        return arr

class PythonSortStrategy(SortStrategy):
    """Uses Python's built-in sort (Timsort)."""
    def sort(self, data: list) -> list:
        return sorted(data)

class ReverseSortStrategy(SortStrategy):
    def sort(self, data: list) -> list:
        return sorted(data, reverse=True)

class Sorter:
    """Context: uses a sort strategy that can be swapped at runtime."""
    def __init__(self, strategy: SortStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: SortStrategy):
        self._strategy = strategy

    def sort(self, data: list) -> list:
        return self._strategy.sort(data)

data = [5, 2, 9, 1, 7, 3]
sorter = Sorter(PythonSortStrategy())
print(f"  Python sort:  {sorter.sort(data)}")

sorter.set_strategy(ReverseSortStrategy())
print(f"  Reverse sort: {sorter.sort(data)}")

sorter.set_strategy(BubbleSortStrategy())
print(f"  Bubble sort:  {sorter.sort(data)}")


# ==============================================================================
# 5. COMMAND PATTERN
# ==============================================================================
# Encapsulates a request as an object, allowing undo/redo operations.

print("\n" + "=" * 45)
print("5. COMMAND")
print("=" * 45)

class Command(ABC):
    @abstractmethod
    def execute(self): ...
    @abstractmethod
    def undo(self): ...

class TextEditor:
    def __init__(self):
        self._text = ""
        self._history: list[Command] = []

    def execute(self, command: Command):
        command.execute()
        self._history.append(command)

    def undo(self):
        if self._history:
            self._history.pop().undo()

    @property
    def text(self): return self._text

class InsertCommand(Command):
    def __init__(self, editor, text: str):
        self._editor = editor
        self._text   = text
    def execute(self):
        self._editor._text += self._text
    def undo(self):
        self._editor._text = self._editor._text[:-len(self._text)]

class DeleteCommand(Command):
    def __init__(self, editor, n: int):
        self._editor = editor
        self._n      = n
        self._deleted = ""
    def execute(self):
        self._deleted = self._editor._text[-self._n:]
        self._editor._text = self._editor._text[:-self._n]
    def undo(self):
        self._editor._text += self._deleted

editor = TextEditor()
editor.execute(InsertCommand(editor, "Hello"))
editor.execute(InsertCommand(editor, ", World"))
print(f"  After inserts: '{editor.text}'")

editor.execute(DeleteCommand(editor, 6))
print(f"  After delete:  '{editor.text}'")

editor.undo()
print(f"  After undo:    '{editor.text}'")

editor.undo()
print(f"  After undo:    '{editor.text}'")
