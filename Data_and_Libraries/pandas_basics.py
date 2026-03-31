"""
Pandas Basics
==============
Pandas is the go-to library for data manipulation and analysis in Python.
It provides DataFrame (table) and Series (column) data structures.

Install: pip install pandas
"""

try:
    import pandas as pd
    import numpy as np
    print(f"Pandas version: {pd.__version__}")
except ImportError:
    print("Install with: pip install pandas numpy")
    exit(1)

# ==============================================================================
# 1. SERIES
# ==============================================================================

print("\n" + "=" * 45)
print("SERIES")
print("=" * 45)

# A Series is a 1D labeled array
s = pd.Series([10, 20, 30, 40, 50], name="scores")
print(s)
print("\nValues:", s.values)
print("Index:", s.index.tolist())
print("Mean:", s.mean())

# Custom index
temps = pd.Series({"Mon": 25, "Tue": 27, "Wed": 22, "Thu": 30, "Fri": 28})
print("\nTemperatures:\n", temps)
print("Wed temp:", temps["Wed"])
print("Above 25:", temps[temps > 25])


# ==============================================================================
# 2. DATAFRAME — CREATION
# ==============================================================================

print("\n" + "=" * 45)
print("DATAFRAME — CREATION")
print("=" * 45)

# From dict
data = {
    "Name":   ["Alice", "Bob", "Charlie", "Diana", "Eve"],
    "Age":    [25, 30, 35, 28, 22],
    "Score":  [88, 75, 92, 65, 97],
    "City":   ["Lusaka", "Kitwe", "Ndola", "Lusaka", "Kitwe"],
    "Passed": [True, True, True, False, True],
}
df = pd.DataFrame(data)
print(df)

print("\nShape:", df.shape)
print("Columns:", df.columns.tolist())
print("Dtypes:\n", df.dtypes)


# ==============================================================================
# 3. SELECTING DATA
# ==============================================================================

print("\n" + "=" * 45)
print("SELECTING DATA")
print("=" * 45)

# Select a column
print("Names:\n", df["Name"])

# Select multiple columns
print("\nName + Score:\n", df[["Name", "Score"]])

# Select rows by label (loc) or integer position (iloc)
print("\nRow 0 (loc):\n", df.loc[0])
print("\nFirst 2 rows (iloc):\n", df.iloc[:2])

# Conditional selection (filtering)
passed = df[df["Passed"] == True]
print("\nPassed students:\n", passed[["Name", "Score"]])

high_scores = df[df["Score"] > 85]
print("\nHigh scores (>85):\n", high_scores[["Name", "Score", "City"]])

# Multiple conditions
lusaka_high = df[(df["City"] == "Lusaka") & (df["Score"] > 70)]
print("\nLusaka students with score > 70:\n", lusaka_high[["Name", "Score"]])


# ==============================================================================
# 4. ADDING AND MODIFYING DATA
# ==============================================================================

print("\n" + "=" * 45)
print("MODIFYING DATA")
print("=" * 45)

# Add a new column
df["Grade"] = df["Score"].apply(
    lambda s: "A" if s >= 90 else ("B" if s >= 80 else ("C" if s >= 70 else "F"))
)
print("With Grade column:\n", df[["Name", "Score", "Grade"]])

# Modify a column
df["Age"] = df["Age"] + 1   # everyone gets one year older
print("\nAges after increment:", df["Age"].tolist())

# Rename columns
df_renamed = df.rename(columns={"Name": "Student", "Score": "Points"})
print("\nRenamed columns:", df_renamed.columns.tolist())


# ==============================================================================
# 5. GROUPBY
# ==============================================================================

print("\n" + "=" * 45)
print("GROUPBY")
print("=" * 45)

print("Average score by city:")
print(df.groupby("City")["Score"].mean())

print("\nCount by city:")
print(df.groupby("City").size())

print("\nMultiple aggregations:")
print(df.groupby("City")["Score"].agg(["mean", "min", "max", "count"]))


# ==============================================================================
# 6. HANDLING MISSING DATA
# ==============================================================================

print("\n" + "=" * 45)
print("MISSING DATA")
print("=" * 45)

df_missing = pd.DataFrame({
    "Name":  ["Alice", "Bob", "Charlie", "Diana"],
    "Score": [88, None, 92, None],
    "City":  ["Lusaka", None, "Ndola", "Kitwe"],
})
print("With missing values:\n", df_missing)
print("\nNull mask:\n", df_missing.isnull())
print("\nNull counts:\n", df_missing.isnull().sum())

# Fill missing values
df_filled = df_missing.fillna({"Score": df_missing["Score"].mean(), "City": "Unknown"})
print("\nAfter fillna:\n", df_filled)

# Drop rows with any missing values
df_dropped = df_missing.dropna()
print("\nAfter dropna:\n", df_dropped)


# ==============================================================================
# 7. MERGING AND JOINING
# ==============================================================================

print("\n" + "=" * 45)
print("MERGING")
print("=" * 45)

students = pd.DataFrame({
    "ID":   [1, 2, 3, 4],
    "Name": ["Alice", "Bob", "Charlie", "Diana"],
})
scores = pd.DataFrame({
    "ID":    [1, 2, 3, 5],
    "Score": [88, 75, 92, 70],
})

print("Inner merge:")
print(pd.merge(students, scores, on="ID", how="inner"))

print("\nLeft merge:")
print(pd.merge(students, scores, on="ID", how="left"))


# ==============================================================================
# 8. STATISTICS
# ==============================================================================

print("\n" + "=" * 45)
print("STATISTICS")
print("=" * 45)

print(df[["Age", "Score"]].describe())
print("\nCorrelation:\n", df[["Age", "Score"]].corr())
