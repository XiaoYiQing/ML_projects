


'''
Slicing arrays
Slicing in python means taking elements from one given index to another given index.

We pass slice instead of index like this: [start:end].

We can also define the step, like this: [start:end:step].

If we don't pass start its considered 0

If we don't pass end its considered length of array in that dimension

If we don't pass step its considered 1
'''

# ======================================================================= >>>>>
#	Array Slicing
# ======================================================================= >>>>>

import numpy as np

arr = np.array([1, 2, 3, 4, 5, 6, 7])
print(f"Original array: {arr}")

print(f"Slice from index [1 to 5[: {arr[1:5]}")
# Note: The result includes the start index, but excludes the end index.

print(f"Slice from index 4 and onward: {arr[4:]}")

print(f"Slice from start up to index 4 (exclusively): {arr[:4]}")

# Negative Array Slicing
print(f"Slice from index [-3 to -1[: {arr[-3:-1]}")

# Step Slicing
print(f"Slice from index [1 to 5[ at steps of 2: {arr[1:5:2]}")
print(f"Every other element through the array: {arr[::2]}")
# ======================================================================= <<<<<

print() 

# ======================================================================= >>>>>
#	2D-Array Slicing
# ======================================================================= >>>>>
arr = np.array([[1, 2, 3, 4, 5], [6, 7, 8, 9, 10]])
print(f"Original 2D-array: \n{arr}")

tar_slice = arr[1, 1:4]
print(f"arr[1, 1:4]: {tar_slice}")

tar_slice = arr[0:2, 2]
print(f"arr[0:2, 2]: {tar_slice}")

tar_slice = arr[0:2, 1:4]
print(f"arr[0:2, 1:4]: \n{tar_slice}")

# ======================================================================= <<<<<
