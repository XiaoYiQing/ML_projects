


'''
NumPy is used to work with arrays. The array object in NumPy is called ndarray.

We can create a NumPy ndarray object by using the array() function.
'''

# ======================================================================= >>>>>
#	Creating Arrays
# ======================================================================= >>>>>

import numpy as np

arr = np.array([1, 2, 3, 4, 5])

print(f"The ndarray: {arr}")
print(f"The array type: {type(arr)}")

# type(): This built-in Python function tells us the type of the object 
# passed to it. Like in above code it shows that arr is numpy.ndarray type.


# To create an ndarray, we can pass a list, tuple or any array-like object 
# into the array() method, and it will be converted into an ndarray:
my_tuple = (1, 2, 3, 4, 5)
arr = np.array( my_tuple )
print(f"The tuple turned ndarray: {arr}")

# ======================================================================= <<<<<


# ======================================================================= >>>>>
#	Dimensions in Arrays
# ======================================================================= >>>>>

'''
A dimension in arrays is one level of array depth (nested arrays).

nested array: are arrays that have arrays as their elements.
'''

# 0-D arrays, or Scalars, are the elements in an array. 
# Each value in an array is a 0-D array.
D0_arr = np.array(42)
print(f"The {D0_arr.ndim}-dim ndarray: {D0_arr}")

# An array that has 0-D arrays as its elements is called uni-dimensional 
# or 1-D array.
# These are the most common and basic arrays.
D1_arr = np.array([1, 42, 3, 4, 5])
print(f"The {D1_arr.ndim}-dim ndarray: {D1_arr}")

# An array that has 1-D arrays as its elements is called a 2-D array.
# These are often used to represent matrix or 2nd order tensors.

# NumPy has a whole sub module dedicated towards matrix operations called numpy.mat
D2_arr = np.array([[1, 2, 3], [4, 5, 6]])
print(f"The {D2_arr.ndim}-dim ndarray: \n{D2_arr}")

# 3-D: arrays
# An array that has 2-D arrays (matrices) as its elements is called 3-D array.
# These are often used to represent a 3rd order tensor.
D3_arr = np.array([[[1, 2, 3], [4, 5, 6]], [[11, 22, 33], [44, 55, 66]]])
print(f"The {D3_arr.ndim}-dim ndarray: \n{D3_arr}")

# ======================================================================= <<<<<

print()

# ======================================================================= >>>>>
#	Higher Dimensional Arrays
# ======================================================================= >>>>>

arr = np.array([1, 2, 3, 4], ndmin=5)
print(f"The {arr.ndim}-dim ndarray: \n{arr}")

# In this array the innermost dimension (5th dim) has 4 elements, the 4th dim 
# has 1 element that is the vector, the 3rd dim has 1 element that is the matrix 
# with the vector, the 2nd dim has 1 element that is 3D array and 1st dim has 
# 1 element that is a 4D array.

# ======================================================================= <<<<<



