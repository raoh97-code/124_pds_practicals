import numpy as np

# Creating a one-dimensional NumPy array
arr1 = np.array([10, 20, 30, 40, 50])

print("One-dimensional array:-")
print(arr1)


# Creating a two-dimensional NumPy array
arr2 = np.array([
    [10, 20, 30],
    [40, 50, 60],
    [70, 80, 90]
])

print("\nTwo-dimensional array:-")
print(arr2)


# Indexing
print("\nIndexing:-\n")
print("Element at row 3, column 2:", arr2[2, 1])
print("First element:", arr2[0, 0])


# Slicing
print("\nSlicing:-\n")

print("First row:")
print(arr2[0, :])

print("First column:")
print(arr2[:, :1])

print("First two rows:")
print(arr2[:2, :])

print("First two columns:")
print(arr2[:, :2])


# Reshaping
print("\nReshaping:-\n")

arr3 = np.arange(1, 13)

print("Original array:")
print(arr3)

reshaped_array = arr3.reshape(3, 4)

print("Reshaped array (3 x 4):")
print(reshaped_array)


# Arithmetic operations
print("\nArithmetic Operations:-\n")

a = np.array([10, 20, 30, 40])
b = np.array([1, 2, 3, 4])

print("Array A:", a)
print("Array B:", b)

print("Addition:", a + b)
print("Subtraction:", a - b)
print("Multiplication:", a * b)
print("Division:", a / b)


# Statistical operations
print("\nStatistical Operations:-\n")

data = np.array([10, 20, 30, 40, 50])

print("Data:", data)
print("Sum:", np.sum(data))
print("Mean:", np.mean(data))
print("Median:", np.median(data))
print("Minimum:", np.min(data))
print("Maximum:", np.max(data))
print("Standard Deviation:", np.std(data))