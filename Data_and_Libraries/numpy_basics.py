"""
NumPy Basics
=============
NumPy (Numerical Python) is the foundation of numerical computing in Python.
It provides fast, efficient multi-dimensional arrays and mathematical functions.

Install: pip install numpy
"""

try:
    import numpy as np
    print(f"NumPy version: {np.__version__}")
except ImportError:
    print("NumPy not installed. Run: pip install numpy")
    exit(1)

# ==============================================================================
# 1. CREATING ARRAYS
# ==============================================================================

print("\n" + "=" * 45)
print("CREATING ARRAYS")
print("=" * 45)

# From a Python list
a1d = np.array([1, 2, 3, 4, 5])
a2d = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

print("1D array:", a1d)
print("2D array:\n", a2d)
print("Shape:", a2d.shape)       # (3, 3)
print("Dtype:", a2d.dtype)       # int64 (platform-dependent)
print("Ndim:", a2d.ndim)         # 2
print("Size:", a2d.size)         # 9 total elements

# Special arrays
zeros   = np.zeros((3, 4))          # array of zeros
ones    = np.ones((2, 3))           # array of ones
eye     = np.eye(3)                  # identity matrix
full    = np.full((2, 2), 7)         # filled with 7
random  = np.random.rand(3, 3)       # random floats [0, 1)
random_int = np.random.randint(0, 10, size=(3, 3))

print("\nzeros(3,4):\n", zeros)
print("eye(3):\n", eye)
print("random(3,3):\n", random.round(3))

# arange and linspace
arr_range  = np.arange(0, 10, 2)         # [0, 2, 4, 6, 8]
arr_linsp  = np.linspace(0, 1, 5)         # [0, 0.25, 0.5, 0.75, 1.0]

print("\narange(0,10,2):", arr_range)
print("linspace(0,1,5):", arr_linsp)


# ==============================================================================
# 2. INDEXING AND SLICING
# ==============================================================================

print("\n" + "=" * 45)
print("INDEXING AND SLICING")
print("=" * 45)

m = np.array([[1, 2, 3],
              [4, 5, 6],
              [7, 8, 9]])

print("m[0, 0]:", m[0, 0])       # 1
print("m[1, 2]:", m[1, 2])       # 6
print("m[-1, -1]:", m[-1, -1])   # 9

# Slicing rows/columns
print("Row 0:", m[0])            # [1, 2, 3]
print("Col 1:", m[:, 1])         # [2, 5, 8]
print("Sub-matrix m[0:2, 1:]:\n", m[0:2, 1:])

# Boolean (fancy) indexing
arr = np.array([10, 20, 30, 40, 50])
mask = arr > 25
print("\nArr:", arr)
print("Mask (>25):", mask)
print("Filtered:", arr[mask])    # [30, 40, 50]
print("Above 25:", arr[arr > 25])


# ==============================================================================
# 3. ARRAY OPERATIONS (VECTORIZED)
# ==============================================================================

print("\n" + "=" * 45)
print("ARRAY OPERATIONS")
print("=" * 45)

a = np.array([1, 2, 3, 4])
b = np.array([10, 20, 30, 40])

print("a + b:", a + b)       # element-wise addition
print("a * b:", a * b)       # element-wise multiplication
print("a ** 2:", a ** 2)     # element-wise power
print("b / a:", b / a)       # element-wise division
print("np.sqrt(a):", np.sqrt(a))

# Broadcasting — smaller array is "broadcast" to match larger
row = np.array([1, 2, 3])       # shape (3,)
col = np.array([[10], [20]])    # shape (2,1)
print("\nBroadcasting:")
print(row + col)                # shape (2,3)


# ==============================================================================
# 4. AGGREGATE FUNCTIONS
# ==============================================================================

print("\n" + "=" * 45)
print("AGGREGATE FUNCTIONS")
print("=" * 45)

data = np.array([[4, 7, 2, 1],
                 [8, 3, 9, 5],
                 [6, 0, 4, 3]])

print("data:\n", data)
print("sum:", np.sum(data))
print("sum axis=0 (per col):", np.sum(data, axis=0))
print("sum axis=1 (per row):", np.sum(data, axis=1))
print("mean:", np.mean(data))
print("std:", np.std(data).round(3))
print("min:", np.min(data))
print("max:", np.max(data))
print("argmin:", np.argmin(data))   # index of global min
print("argmax:", np.argmax(data))   # index of global max


# ==============================================================================
# 5. RESHAPING AND STACKING
# ==============================================================================

print("\n" + "=" * 45)
print("RESHAPING AND STACKING")
print("=" * 45)

arr = np.arange(12)
print("Original:", arr)
print("Reshape (3,4):\n", arr.reshape(3, 4))
print("Reshape (2,6):\n", arr.reshape(2, 6))
print("Flatten:", arr.reshape(3, 4).flatten())

# Transpose
matrix = np.array([[1, 2, 3], [4, 5, 6]])
print("\nMatrix:\n", matrix)
print("Transposed:\n", matrix.T)

# Stacking
a = np.array([1, 2, 3])
b = np.array([4, 5, 6])
print("\nvstack:\n", np.vstack([a, b]))
print("hstack:", np.hstack([a, b]))


# ==============================================================================
# 6. LINEAR ALGEBRA
# ==============================================================================

print("\n" + "=" * 45)
print("LINEAR ALGEBRA")
print("=" * 45)

A = np.array([[2, 1], [1, 3]])
B = np.array([[1, 2], [3, 4]])

print("A @ B (matrix multiply):\n", A @ B)
print("det(A):", np.linalg.det(A))
print("inv(A):\n", np.linalg.inv(A).round(3))

eigenvalues, eigenvectors = np.linalg.eig(A)
print("Eigenvalues:", eigenvalues)
