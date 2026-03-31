"""
Mini Project — Data Analysis Demo
====================================
Demonstrates a complete data analysis workflow using NumPy and Pandas.

Skills: NumPy, Pandas, statistics, data cleaning, groupby, formatting
"""

try:
    import numpy as np
    import pandas as pd
except ImportError:
    print("Install with: pip install numpy pandas")
    exit(1)

import random
import statistics

random.seed(42)
np.random.seed(42)

print("=" * 55)
print("  📊  STUDENT PERFORMANCE DATA ANALYSIS")
print("=" * 55)

# ==============================================================================
# 1. GENERATE SAMPLE DATASET
# ==============================================================================

n = 200
cities   = ["Lusaka", "Kitwe", "Ndola", "Livingstone", "Chipata"]
subjects = ["Math", "Science", "English", "History", "Computer"]
genders  = ["Male", "Female"]

data = {
    "student_id":   range(1, n + 1),
    "name":         [f"Student_{i:03d}" for i in range(1, n + 1)],
    "city":         np.random.choice(cities, n),
    "gender":       np.random.choice(genders, n),
    "age":          np.random.randint(16, 21, n),
    "study_hours":  np.round(np.random.uniform(1, 8, n), 1),
    "math":         np.random.randint(40, 100, n),
    "science":      np.random.randint(35, 100, n),
    "english":      np.random.randint(45, 100, n),
    "history":      np.random.randint(40, 100, n),
    "computer":     np.random.randint(50, 100, n),
}

df = pd.DataFrame(data)

# Add some missing values to practice cleaning
random_indices = np.random.choice(df.index, 10, replace=False)
df.loc[random_indices[:5], "math"]    = np.nan
df.loc[random_indices[5:], "english"] = np.nan

print(f"\nDataset shape: {df.shape}")
print(df.head())


# ==============================================================================
# 2. DATA CLEANING
# ==============================================================================

print("\n" + "-" * 55)
print("2. DATA CLEANING")
print("-" * 55)

# Check for missing values
missing = df.isnull().sum()
print("Missing values per column:")
print(missing[missing > 0])

# Fill missing numerical values with column median
for col in ["math", "english"]:
    median = df[col].median()
    df[col] = df[col].fillna(median)
    print(f"  Filled {col} NaN with median={median:.1f}")

print(f"  Missing after fill: {df.isnull().sum().sum()}")


# ==============================================================================
# 3. FEATURE ENGINEERING
# ==============================================================================

print("\n" + "-" * 55)
print("3. FEATURE ENGINEERING")
print("-" * 55)

subject_cols = ["math", "science", "english", "history", "computer"]

# Calculate average score
df["average"] = df[subject_cols].mean(axis=1).round(2)

# Assign letter grade
def assign_grade(avg):
    if avg >= 90: return "A"
    if avg >= 80: return "B"
    if avg >= 70: return "C"
    if avg >= 60: return "D"
    return "F"

df["grade"]  = df["average"].apply(assign_grade)
df["passed"] = df["average"] >= 60

print("New columns added: average, grade, passed")
print(df[["name", "average", "grade", "passed"]].head())


# ==============================================================================
# 4. SUMMARY STATISTICS
# ==============================================================================

print("\n" + "-" * 55)
print("4. SUMMARY STATISTICS")
print("-" * 55)

print("\nOverall Subject Averages:")
print(df[subject_cols].mean().round(2).to_string())

print("\nDescriptive Statistics for Average Score:")
print(df["average"].describe().round(2))

print(f"\nPass Rate: {df['passed'].mean() * 100:.1f}%")
print(f"Total Students: {len(df)}")
print(f"Passing: {df['passed'].sum()}")
print(f"Failing: {(~df['passed']).sum()}")


# ==============================================================================
# 5. GROUP ANALYSIS
# ==============================================================================

print("\n" + "-" * 55)
print("5. GROUP ANALYSIS")
print("-" * 55)

print("\nAverage score by city:")
city_avg = df.groupby("city")["average"].agg(["mean", "count", "std"])
city_avg.columns = ["avg_score", "students", "std_dev"]
city_avg = city_avg.sort_values("avg_score", ascending=False).round(2)
print(city_avg)

print("\nAverage score by gender:")
print(df.groupby("gender")["average"].mean().round(2))

print("\nGrade distribution:")
grade_counts = df["grade"].value_counts().reindex(["A", "B", "C", "D", "F"])
for grade, count in grade_counts.items():
    bar = "█" * int(count / len(df) * 40)
    print(f"  {grade}: {bar:<40} {count:3d} ({count/len(df)*100:.1f}%)")


# ==============================================================================
# 6. CORRELATION ANALYSIS
# ==============================================================================

print("\n" + "-" * 55)
print("6. CORRELATION ANALYSIS")
print("-" * 55)

corr_matrix = df[subject_cols + ["study_hours", "average"]].corr()["average"]
print("Correlation with average score:")
print(corr_matrix.sort_values(ascending=False).round(3))


# ==============================================================================
# 7. TOP PERFORMERS
# ==============================================================================

print("\n" + "-" * 55)
print("7. TOP 10 PERFORMERS")
print("-" * 55)

top_10 = df.nlargest(10, "average")[["name", "city", "average", "grade", "study_hours"]]
top_10.index = range(1, 11)
print(top_10.to_string())

print("\n" + "=" * 55)
print("Analysis complete!")
