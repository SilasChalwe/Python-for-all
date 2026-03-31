"""
03 - Context Managers
======================
This file covers:
  - The 'with' statement and why it matters
  - The context manager protocol: __enter__ and __exit__
  - Creating context managers with classes
  - Creating context managers with @contextlib.contextmanager
  - Multiple context managers in one 'with' statement
  - Practical use cases
"""

import contextlib
import time
import os
import tempfile

# ==============================================================================
# 1. WHY CONTEXT MANAGERS?
# ==============================================================================
# Context managers guarantee that cleanup code runs, even if an exception
# is raised. The most common use is file handling.

print("=" * 45)
print("WHY CONTEXT MANAGERS?")
print("=" * 45)

# WITHOUT context manager (problematic):
# f = open("file.txt")
# data = f.read()     # if this raises, f.close() never runs!
# f.close()

# WITH context manager (safe):
# with open("file.txt") as f:
#     data = f.read()
# f is automatically closed here, even on exception

tmpdir = tempfile.mkdtemp()
tmpfile = os.path.join(tmpdir, "test.txt")

with open(tmpfile, "w") as f:
    f.write("Hello, context manager!")

with open(tmpfile, "r") as f:
    print("File content:", f.read())


# ==============================================================================
# 2. THE CONTEXT MANAGER PROTOCOL
# ==============================================================================
# An object is a context manager if it defines:
#   __enter__(self)          → called when entering the 'with' block
#   __exit__(self, exc_type, exc_val, exc_tb) → called when exiting

print("\n--- Context Manager Protocol ---")

class Timer:
    """Context manager that measures elapsed time."""

    def __enter__(self):
        self._start = time.perf_counter()
        return self   # value bound to 'as' variable

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.elapsed = time.perf_counter() - self._start
        print(f"  Elapsed: {self.elapsed:.6f}s")
        return False  # False = don't suppress exceptions

with Timer() as t:
    total = sum(range(1_000_000))

print(f"  Sum: {total}")
# t.elapsed is available after the block


class ManagedFile:
    """Custom context manager for file handling."""

    def __init__(self, filename, mode="r"):
        self.filename = filename
        self.mode     = mode
        self.file     = None

    def __enter__(self):
        self.file = open(self.filename, self.mode)
        return self.file

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.file:
            self.file.close()
            print("  File closed automatically.")
        # Return True to suppress exceptions, False (or None) to propagate
        return False

with ManagedFile(tmpfile, "r") as f:
    content = f.read()
    print(f"  Read: {content}")


# ==============================================================================
# 3. @contextlib.contextmanager DECORATOR
# ==============================================================================
# A simpler way to write context managers using a generator function.
# Everything before 'yield' is __enter__, everything after is __exit__.

print("\n--- @contextmanager ---")

@contextlib.contextmanager
def managed_timer(label: str):
    """Context manager: time a code block with a label."""
    start = time.perf_counter()
    try:
        yield   # control goes to the 'with' block here
    finally:
        elapsed = time.perf_counter() - start
        print(f"  [{label}] took {elapsed:.6f}s")

with managed_timer("loop"):
    total = sum(range(500_000))

@contextlib.contextmanager
def temp_directory():
    """Create a temporary directory and clean it up afterwards."""
    import shutil
    directory = tempfile.mkdtemp()
    try:
        print(f"  Created temp dir: {directory}")
        yield directory
    finally:
        shutil.rmtree(directory)
        print(f"  Cleaned up temp dir: {directory}")

with temp_directory() as d:
    filepath = os.path.join(d, "data.txt")
    with open(filepath, "w") as f:
        f.write("temporary data")
    print(f"  File exists: {os.path.exists(filepath)}")

print(f"  Temp dir gone: {not os.path.exists(d)}")


# ==============================================================================
# 4. MULTIPLE CONTEXT MANAGERS
# ==============================================================================

print("\n--- Multiple Context Managers ---")

file1 = os.path.join(tmpdir, "file1.txt")
file2 = os.path.join(tmpdir, "file2.txt")

with open(file1, "w") as f1, open(file2, "w") as f2:
    f1.write("Content of file 1")
    f2.write("Content of file 2")

print("  Both files written successfully.")


# ==============================================================================
# 5. contextlib UTILITIES
# ==============================================================================

print("\n--- contextlib Utilities ---")

# suppress — silence specific exceptions
with contextlib.suppress(FileNotFoundError):
    os.remove("/nonexistent/file.txt")   # would raise, but is suppressed

print("  FileNotFoundError suppressed.")

# nullcontext — a no-op context manager (useful in conditional logic)
debug_mode = False
ctx = managed_timer("conditional") if debug_mode else contextlib.nullcontext()

with ctx:
    result = sum(range(100))

# redirect_stdout — capture print output
import io
buffer = io.StringIO()
with contextlib.redirect_stdout(buffer):
    print("This goes to the buffer, not the terminal.")
captured = buffer.getvalue()
print(f"  Captured output: {captured.strip()!r}")


# ==============================================================================
# 6. EXCEPTION HANDLING IN __exit__
# ==============================================================================

print("\n--- Exception Handling in Context Managers ---")

class SuppressErrors:
    """Context manager that suppresses specified exceptions."""

    def __init__(self, *exceptions):
        self.exceptions = exceptions

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type and issubclass(exc_type, self.exceptions):
            print(f"  Suppressed: {exc_type.__name__}: {exc_val}")
            return True   # suppress the exception
        return False       # propagate other exceptions

with SuppressErrors(ZeroDivisionError, ValueError):
    result = 1 / 0   # suppressed!

print("  Continued after suppressed exception.")
