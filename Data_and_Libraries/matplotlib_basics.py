"""
Matplotlib Basics
==================
Matplotlib is the most widely used plotting library in Python.
It produces publication-quality figures in a variety of formats.

Install: pip install matplotlib
"""

try:
    import matplotlib
    matplotlib.use("Agg")   # non-interactive backend (no display needed)
    import matplotlib.pyplot as plt
    import numpy as np
    print(f"Matplotlib version: {matplotlib.__version__}")
except ImportError:
    print("Install with: pip install matplotlib numpy")
    exit(1)

import os
import tempfile
OUTDIR = tempfile.mkdtemp()
print(f"Saving plots to: {OUTDIR}\n")

# ==============================================================================
# 1. LINE PLOT
# ==============================================================================

print("Creating line plot...")
x = np.linspace(0, 2 * np.pi, 100)
y_sin = np.sin(x)
y_cos = np.cos(x)

fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(x, y_sin, label="sin(x)", color="blue",  linewidth=2)
ax.plot(x, y_cos, label="cos(x)", color="orange", linewidth=2, linestyle="--")

ax.set_title("Sine and Cosine Waves", fontsize=14)
ax.set_xlabel("x (radians)")
ax.set_ylabel("y")
ax.legend()
ax.grid(True, alpha=0.3)
ax.axhline(0, color="black", linewidth=0.5)

plt.tight_layout()
plt.savefig(os.path.join(OUTDIR, "01_line_plot.png"), dpi=100)
plt.close()
print("  Saved: 01_line_plot.png")


# ==============================================================================
# 2. BAR CHART
# ==============================================================================

print("Creating bar chart...")
categories = ["Python", "JavaScript", "Java", "C++", "Rust"]
values     = [32.5, 22.4, 18.2, 10.1, 7.8]   # popularity (%)
colors     = ["#4C72B0", "#DD8452", "#55A868", "#C44E52", "#8172B2"]

fig, ax = plt.subplots(figsize=(8, 5))
bars = ax.bar(categories, values, color=colors, edgecolor="white", linewidth=1.2)

# Add value labels on top of each bar
for bar, val in zip(bars, values):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.3,
            f"{val}%", ha="center", va="bottom", fontsize=10)

ax.set_title("Programming Language Popularity", fontsize=14)
ax.set_xlabel("Language")
ax.set_ylabel("Popularity (%)")
ax.set_ylim(0, max(values) + 5)
ax.grid(axis="y", alpha=0.3)

plt.tight_layout()
plt.savefig(os.path.join(OUTDIR, "02_bar_chart.png"), dpi=100)
plt.close()
print("  Saved: 02_bar_chart.png")


# ==============================================================================
# 3. SCATTER PLOT
# ==============================================================================

print("Creating scatter plot...")
np.random.seed(42)
n = 100
x = np.random.randn(n)
y = 2 * x + np.random.randn(n) * 0.8
colors_scatter = np.where(x > 0, "steelblue", "coral")

fig, ax = plt.subplots(figsize=(7, 5))
scatter = ax.scatter(x, y, c=colors_scatter, alpha=0.7, s=60, edgecolors="white", linewidths=0.5)

# Add trend line
z = np.polyfit(x, y, 1)
p = np.poly1d(z)
x_line = np.linspace(x.min(), x.max(), 100)
ax.plot(x_line, p(x_line), "k--", linewidth=1.5, label=f"Trend: y={z[0]:.2f}x+{z[1]:.2f}")

ax.set_title("Scatter Plot with Trend Line", fontsize=14)
ax.set_xlabel("X variable")
ax.set_ylabel("Y variable")
ax.legend()
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(os.path.join(OUTDIR, "03_scatter_plot.png"), dpi=100)
plt.close()
print("  Saved: 03_scatter_plot.png")


# ==============================================================================
# 4. HISTOGRAM
# ==============================================================================

print("Creating histogram...")
np.random.seed(0)
data = np.concatenate([np.random.normal(0, 1, 500), np.random.normal(4, 0.8, 300)])

fig, ax = plt.subplots(figsize=(8, 5))
n_bins, bins, patches = ax.hist(data, bins=40, color="steelblue",
                                 edgecolor="white", alpha=0.8)

# Color bars by value
for patch, x_left in zip(patches, bins):
    patch.set_facecolor("steelblue" if x_left < 2 else "coral")

ax.axvline(data.mean(), color="black",    linestyle="--", label=f"Mean={data.mean():.2f}")
ax.axvline(np.median(data), color="green", linestyle=":",  label=f"Median={np.median(data):.2f}")

ax.set_title("Histogram with Mean and Median", fontsize=14)
ax.set_xlabel("Value")
ax.set_ylabel("Frequency")
ax.legend()
ax.grid(axis="y", alpha=0.3)

plt.tight_layout()
plt.savefig(os.path.join(OUTDIR, "04_histogram.png"), dpi=100)
plt.close()
print("  Saved: 04_histogram.png")


# ==============================================================================
# 5. SUBPLOTS
# ==============================================================================

print("Creating subplot grid...")
fig, axes = plt.subplots(2, 2, figsize=(10, 8))
fig.suptitle("Multiple Plots", fontsize=16, fontweight="bold")

x = np.linspace(0, 4 * np.pi, 200)

# Top-left: sine
axes[0, 0].plot(x, np.sin(x), color="blue")
axes[0, 0].set_title("Sine")
axes[0, 0].grid(alpha=0.3)

# Top-right: cosine
axes[0, 1].plot(x, np.cos(x), color="orange")
axes[0, 1].set_title("Cosine")
axes[0, 1].grid(alpha=0.3)

# Bottom-left: exp decay
axes[1, 0].plot(x, np.exp(-x / 5) * np.sin(x), color="green")
axes[1, 0].set_title("Damped Sine")
axes[1, 0].grid(alpha=0.3)

# Bottom-right: bar chart
categories = ["A", "B", "C", "D"]
vals = [4, 7, 2, 9]
axes[1, 1].bar(categories, vals, color=["#4C72B0","#DD8452","#55A868","#C44E52"])
axes[1, 1].set_title("Bar Chart")
axes[1, 1].grid(axis="y", alpha=0.3)

plt.tight_layout()
plt.savefig(os.path.join(OUTDIR, "05_subplots.png"), dpi=100)
plt.close()
print("  Saved: 05_subplots.png")


# ==============================================================================
# 6. PIE CHART
# ==============================================================================

print("Creating pie chart...")
sizes  = [35, 25, 20, 15, 5]
labels = ["Python", "JavaScript", "Java", "C++", "Other"]
explode = (0.05, 0, 0, 0, 0)   # explode the first slice

fig, ax = plt.subplots(figsize=(7, 7))
wedges, texts, autotexts = ax.pie(
    sizes, explode=explode, labels=labels, autopct="%1.1f%%",
    shadow=True, startangle=90
)
for autotext in autotexts:
    autotext.set_fontsize(10)

ax.set_title("Language Market Share", fontsize=14)
plt.tight_layout()
plt.savefig(os.path.join(OUTDIR, "06_pie_chart.png"), dpi=100)
plt.close()
print("  Saved: 06_pie_chart.png")

print(f"\nAll plots saved to: {OUTDIR}")
print("Note: In a Jupyter notebook, use plt.show() instead of plt.savefig()")
