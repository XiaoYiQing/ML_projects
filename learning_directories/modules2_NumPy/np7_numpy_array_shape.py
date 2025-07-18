


'''
Shape of an Array
The shape of an array is the number of elements in each dimension.

Get the Shape of an Array
NumPy arrays have an attribute called "shape" that returns a tuple with 
each index having the number of corresponding elements.
'''

# ======================================================================= >>>>>
#	Array Shape
# ======================================================================= >>>>>

import numpy as np

arr = np.array([[1, 2, 3, 4], [5, 6, 7, 8]])

print(f"Array shape: {arr.shape}")

str_var = "The example above returns (2, 4), which means that the array \
has 2 dimensions, where the first dimension has 2 elements and the second has 4."
print( str_var )

print()

# Create an array with 5 dimensions using ndmin using a vector with values 1,2,3,4 
# and verify that last dimension has value 4:
arr = np.array([1, 2, 3, 4], ndmin=5)
print(f"Array shape: {arr.shape}")
# ======================================================================= <<<<<



