"""
03 - File Handling
===================
This file covers:
  - Opening files with open() and the 'with' statement
  - Read, write, and append modes
  - Reading entire file, line by line, readlines()
  - Writing to files
  - os.path operations
  - JSON read/write
  - CSV read/write using the csv module
"""

import os
import json
import csv
import tempfile

# We will use a temporary directory so this script leaves no side effects
TMPDIR = tempfile.mkdtemp()
print(f"Working in temp directory: {TMPDIR}\n")

# ==============================================================================
# 1. WRITING FILES
# ==============================================================================

print("=" * 40)
print("WRITING FILES")
print("=" * 40)

sample_file = os.path.join(TMPDIR, "sample.txt")

# 'w' mode — write (creates file, overwrites if exists)
with open(sample_file, "w") as f:
    f.write("Line 1: Hello, Python!\n")
    f.write("Line 2: File handling is easy.\n")
    f.write("Line 3: Always use the 'with' statement.\n")

print(f"Written to: {sample_file}")

# 'a' mode — append (adds to end of file, does not overwrite)
with open(sample_file, "a") as f:
    f.write("Line 4: This was appended.\n")

print("Appended a line.")

# Writing multiple lines at once with writelines()
more_file = os.path.join(TMPDIR, "more.txt")
lines = ["apple\n", "banana\n", "cherry\n"]
with open(more_file, "w") as f:
    f.writelines(lines)

print(f"Written list to: {more_file}")


# ==============================================================================
# 2. READING FILES
# ==============================================================================

print("\n" + "=" * 40)
print("READING FILES")
print("=" * 40)

# read() — entire file as one string
with open(sample_file, "r") as f:
    content = f.read()
print("read():\n", content)

# readline() — one line at a time
with open(sample_file, "r") as f:
    first_line  = f.readline()
    second_line = f.readline()
print("readline():")
print("  First:", first_line.strip())
print("  Second:", second_line.strip())

# readlines() — all lines as a list
with open(sample_file, "r") as f:
    lines = f.readlines()
print(f"\nreadlines() → {len(lines)} lines")

# Iterating line by line (most memory-efficient for large files)
print("Line by line iteration:")
with open(sample_file, "r") as f:
    for i, line in enumerate(f, start=1):
        print(f"  [{i}] {line.strip()}")


# ==============================================================================
# 3. FILE MODES SUMMARY
# ==============================================================================

print("\n--- File Modes ---")
modes = {
    "r":  "Read (default). Error if file doesn't exist.",
    "w":  "Write. Creates file; overwrites if exists.",
    "a":  "Append. Creates file; adds to end if exists.",
    "x":  "Exclusive create. Error if file already exists.",
    "rb": "Read in binary mode.",
    "wb": "Write in binary mode.",
    "r+": "Read and write.",
}
for mode, desc in modes.items():
    print(f"  '{mode}': {desc}")


# ==============================================================================
# 4. os.path OPERATIONS
# ==============================================================================

print("\n" + "=" * 40)
print("os.path OPERATIONS")
print("=" * 40)

print(f"File exists: {os.path.exists(sample_file)}")
print(f"Is file:     {os.path.isfile(sample_file)}")
print(f"Is dir:      {os.path.isdir(sample_file)}")
print(f"File size:   {os.path.getsize(sample_file)} bytes")
print(f"Dirname:     {os.path.dirname(sample_file)}")
print(f"Basename:    {os.path.basename(sample_file)}")
name, ext = os.path.splitext(sample_file)
print(f"Name: {name}  Ext: {ext}")

# Joining paths (always use os.path.join, not string concatenation)
new_path = os.path.join(TMPDIR, "subdir", "data.txt")
print(f"Joined path: {new_path}")

# List files in a directory
print(f"\nFiles in temp dir: {os.listdir(TMPDIR)}")

# Create a subdirectory
subdir = os.path.join(TMPDIR, "subdir")
os.makedirs(subdir, exist_ok=True)   # exist_ok=True prevents error if exists
print(f"Created: {subdir}")


# ==============================================================================
# 5. JSON FILES
# ==============================================================================

print("\n" + "=" * 40)
print("JSON FILES")
print("=" * 40)

json_file = os.path.join(TMPDIR, "data.json")

# Writing JSON
person = {
    "name": "SilasChalwe",
    "age": 25,
    "skills": ["Python", "JavaScript", "SQL"],
    "active": True,
    "score": 98.5
}

with open(json_file, "w") as f:
    json.dump(person, f, indent=4)   # indent for pretty-printing

print(f"JSON written to: {json_file}")

# Reading JSON
with open(json_file, "r") as f:
    loaded = json.load(f)

print(f"Loaded name: {loaded['name']}")
print(f"Skills: {loaded['skills']}")

# Convert to/from JSON strings (without files)
json_str = json.dumps(person, indent=2)
print("\nJSON string:\n", json_str[:100], "...")

back = json.loads(json_str)
print("Parsed from string:", back["name"])


# ==============================================================================
# 6. CSV FILES
# ==============================================================================

print("\n" + "=" * 40)
print("CSV FILES")
print("=" * 40)

csv_file = os.path.join(TMPDIR, "students.csv")

# Writing CSV
students = [
    ["Name", "Score", "Grade"],
    ["Alice",  92, "A"],
    ["Bob",    75, "B"],
    ["Charlie", 60, "D"],
    ["Diana",  88, "B"],
]

with open(csv_file, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(students)

print(f"CSV written: {csv_file}")

# Reading CSV
with open(csv_file, "r") as f:
    reader = csv.reader(f)
    for row in reader:
        print("  ", row)

# Using DictReader/DictWriter for cleaner code
print("\nUsing DictReader:")
with open(csv_file, "r") as f:
    dict_reader = csv.DictReader(f)
    for row in dict_reader:
        print(f"  {row['Name']}: {row['Score']} ({row['Grade']})")
