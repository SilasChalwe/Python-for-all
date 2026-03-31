"""
Seaborn Basics
===============
Seaborn is a statistical data visualization library built on Matplotlib.
It provides beautiful default styles and high-level plotting functions.

Install: pip install seaborn matplotlib pandas numpy
"""

try:
    import seaborn as sns
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import pandas as pd
    import numpy as np
    print(f"Seaborn version: {sns.__version__}")
except ImportError:
    print("Install with: pip install seaborn matplotlib pandas numpy")
    exit(1)

import os, tempfile
OUTDIR = tempfile.mkdtemp()

# Set seaborn theme
sns.set_theme(style="whitegrid", palette="muted")
print(f"Saving plots to: {OUTDIR}\n")

# ==============================================================================
# SAMPLE DATASET
# ==============================================================================

np.random.seed(42)
n = 150

df = pd.DataFrame({
    "study_hours": np.random.uniform(1, 8, n),
    "sleep_hours": np.random.uniform(4, 10, n),
    "score":       None,
    "grade":       None,
    "city":        np.random.choice(["Lusaka", "Kitwe", "Ndola"], n),
    "gender":      np.random.choice(["Male", "Female"], n),
})
# Simulate score as a function of study hours + noise
df["score"] = (
    40 + 7 * df["study_hours"] + 2 * df["sleep_hours"] + np.random.normal(0, 5, n)
).clip(0, 100).round(1)
df["grade"] = pd.cut(df["score"], bins=[0, 60, 70, 80, 90, 100],
                     labels=["F", "D", "C", "B", "A"])


# ==============================================================================
# 1. HISTPLOT (Distribution)
# ==============================================================================

print("Creating histplot...")
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

sns.histplot(df["score"], bins=20, kde=True, ax=axes[0], color="steelblue")
axes[0].set_title("Score Distribution")

sns.histplot(data=df, x="score", hue="grade", multiple="stack",
             bins=20, ax=axes[1])
axes[1].set_title("Score by Grade")

plt.tight_layout()
plt.savefig(os.path.join(OUTDIR, "01_histplot.png"), dpi=100)
plt.close()
print("  Saved: 01_histplot.png")


# ==============================================================================
# 2. BOXPLOT
# ==============================================================================

print("Creating boxplot...")
fig, ax = plt.subplots(figsize=(8, 5))
sns.boxplot(data=df, x="grade", y="score", palette="Set2",
            order=["A", "B", "C", "D", "F"], ax=ax)
sns.stripplot(data=df, x="grade", y="score", color="black", alpha=0.2,
              order=["A", "B", "C", "D", "F"], size=3, ax=ax)
ax.set_title("Score Distribution by Grade")
plt.tight_layout()
plt.savefig(os.path.join(OUTDIR, "02_boxplot.png"), dpi=100)
plt.close()
print("  Saved: 02_boxplot.png")


# ==============================================================================
# 3. SCATTER PLOT WITH REGRESSION LINE
# ==============================================================================

print("Creating scatter + regression...")
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

sns.regplot(data=df, x="study_hours", y="score", ax=axes[0],
            scatter_kws={"alpha": 0.4}, line_kws={"color": "red"})
axes[0].set_title("Study Hours vs Score")

sns.scatterplot(data=df, x="study_hours", y="score", hue="grade",
                style="gender", alpha=0.7, ax=axes[1])
axes[1].set_title("Study Hours vs Score (by Grade & Gender)")

plt.tight_layout()
plt.savefig(os.path.join(OUTDIR, "03_scatter.png"), dpi=100)
plt.close()
print("  Saved: 03_scatter.png")


# ==============================================================================
# 4. HEATMAP (Correlation Matrix)
# ==============================================================================

print("Creating heatmap...")
corr = df[["study_hours", "sleep_hours", "score"]].corr()

fig, ax = plt.subplots(figsize=(6, 5))
sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm",
            linewidths=0.5, square=True, ax=ax)
ax.set_title("Correlation Heatmap")
plt.tight_layout()
plt.savefig(os.path.join(OUTDIR, "04_heatmap.png"), dpi=100)
plt.close()
print("  Saved: 04_heatmap.png")


# ==============================================================================
# 5. BARPLOT AND COUNTPLOT
# ==============================================================================

print("Creating barplot and countplot...")
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Average score per city
sns.barplot(data=df, x="city", y="score", palette="Set1",
            errorbar="sd", ax=axes[0])
axes[0].set_title("Average Score by City")

# Count of each grade
sns.countplot(data=df, x="grade", order=["A", "B", "C", "D", "F"],
              palette="viridis", ax=axes[1])
axes[1].set_title("Count by Grade")

plt.tight_layout()
plt.savefig(os.path.join(OUTDIR, "05_bar_count.png"), dpi=100)
plt.close()
print("  Saved: 05_bar_count.png")


# ==============================================================================
# 6. PAIRPLOT
# ==============================================================================

print("Creating pairplot (may take a moment)...")
pairplot_df = df[["study_hours", "sleep_hours", "score", "grade"]].copy()

g = sns.pairplot(pairplot_df, hue="grade", vars=["study_hours", "sleep_hours", "score"],
                 plot_kws={"alpha": 0.5})
g.fig.suptitle("Pairplot", y=1.02)
plt.savefig(os.path.join(OUTDIR, "06_pairplot.png"), dpi=100, bbox_inches="tight")
plt.close()
print("  Saved: 06_pairplot.png")

print(f"\nAll plots saved to: {OUTDIR}")
