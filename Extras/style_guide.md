# Python Style Guide (PEP 8 Summary)

## Indentation
- Use **4 spaces** per indentation level (never tabs).

## Line Length
- Maximum **79 characters** per line.
- Docstrings and comments: max **72 characters**.

## Blank Lines
- 2 blank lines around top-level functions and classes.
- 1 blank line between methods inside a class.

## Imports
```python
# Standard library first
import os
import sys

# Third-party next
import requests
import numpy as np

# Local last
from mymodule import MyClass
```
- One import per line. Never `import os, sys`.

## Naming Conventions
| Type | Convention | Example |
|------|-----------|---------|
| Variable | snake_case | `user_name` |
| Function | snake_case | `get_data()` |
| Class | PascalCase | `UserAccount` |
| Constant | UPPER_SNAKE | `MAX_SIZE` |
| Module | snake_case | `my_module.py` |
| Private | _leading_underscore | `_helper()` |

## Whitespace
```python
# Correct
x = 1
y = x + 1
func(a, b)
d = {"key": "value"}

# Wrong
x=1
func( a,b )
d = {"key" : "value"}
```

## Strings
- Use consistent quotes (single or double — pick one).
- Use f-strings for formatting: `f"Hello, {name}!"`

## Comments
- Comments should be complete sentences.
- Use `#` with a single space: `# This is a comment`
- Avoid obvious comments: don't say `x = x + 1  # increment x`

## Docstrings
```python
def add(a, b):
    """Return the sum of a and b."""
    return a + b
```

## Comparisons
```python
# Use 'is' for None, True, False
if x is None: ...
if flag is True: ...  # or just: if flag:

# Use == for values
if name == "Alice": ...

# Don't compare booleans with ==
if success:         # not: if success == True:
if not error:       # not: if error == False:
```

## Tools
- **pycodestyle** / **flake8** — check PEP 8 compliance
- **black** — auto-format code
- **isort** — sort imports
- **pylint** / **mypy** — static analysis and type checking
