


'''
Splitting is reverse operation of Joining.

Joining merges multiple arrays into one and Splitting breaks one array 
into multiple.
'''


# ======================================================================= >>>>>
#	Splitting NumPy Arrays
# ======================================================================= >>>>>

import numpy as np

'''
We use array_split() for splitting arrays, we pass it the array we want 
to split and the number of splits.
'''

arr = np.array([1, 2, 3, 4, 5, 6])
print( f"Array = {arr}" )

# Split the array into 3 sub arrays.
newarr = np.array_split(arr, 3)
print(f"Array array_split in 3: {newarr}")
# Note: The return value is a list containing three arrays.

# If the array has less elements than required, it will adjust from the end accordingly.
newarr = np.array_split(arr, 4)
print(f"Array array_split in 4: {newarr}")

'''
Note: We also have the method split() available but it will not adjust the 
elements when elements are less in source array for splitting like in example 
above, array_split() worked properly but split() would fail.
'''
# ======================================================================= <<<<<


# ======================================================================= >>>>>
#	Splitting NumPy Arrays: 2D Arrays
# ======================================================================= >>>>>

'''
Use the same syntax when splitting 2-D arrays.

Use the array_split() method, pass in the array you want to split and the 
number of splits you want to do.
'''

arr = np.array([[1, 2], [3, 4], [5, 6], [7, 8], [9, 10], [11, 12]])
newarr = np.array_split(arr, 3)
print(f"2D-split along axis 0 (Sub-array index 0): \n{newarr[0]}")

# You can specify the axis along which to split:
newarr = np.array_split(arr, 3, axis=1)
print(f"2D-split along axis 1 (Sub-array index 0): \n{newarr[0]}")

# An alternate solution is using hsplit() opposite of hstack()
newarr = np.hsplit(arr, 2)
print(f"2D-hsplit (Sub-array index 0): \n{newarr[0]}")

newarr = np.vsplit(arr, 3)
print(f"2D-vsplit (Sub-array index 0): \n{newarr[0]}")

# Note: Similar alternates to vstack() and dstack() are available as 
#   vsplit() and dsplit().
# ======================================================================= <<<<<





