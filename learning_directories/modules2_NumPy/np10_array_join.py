


'''
Joining means putting contents of two or more arrays in a single array.

In SQL we join tables based on a key, whereas in NumPy we join arrays by axes.
'''


# ======================================================================= >>>>>
#	Array Join: Concatenate
# ======================================================================= >>>>>

import numpy as np

'''
We pass a sequence of arrays that we want to join to the concatenate() function, 
along with the axis. If axis is not explicitly passed, it is taken as 0.
'''

arr1 = np.array([1, 2, 3, 4])
arr2 = np.array([5, 6, 7, 8])
axis = 0
arr = np.concatenate((arr1, arr2), axis=axis)
print(f"1D concatenate along axis {axis}: \n{arr}")
# Axis 0 is the horizontal, thus continuing the horizontal unto arr2.

'''
NOTE:
Axes are numbered left to right; axis 0 is the first element in the shape tuple.

In 1D case, there is no distinction since there is only 1 axis. Technically,
    we only have a row vector, so the axis 0 goes along the columns.
In 2D case, axis 0 goes along rows and axis 1 goes along columns.
In 3D case, arrays are arranged as an 1D array of 2D arrays, in which case, the
    so called 'row' and 'columns' are pushed to axis 1 and 2, respectively.
    Axis 0 now follows indexing of the 2D sub-arrays.
Further higher dimension follows this logic: all previous axis push up by 1,  
    axis 0 follows the newly added dimension.
'''

# Join two 2-D arrays along rows (axis=1, i.e. columns):
arr1 = np.array([[1, 2, -1], [3, 4, -3]])
arr2 = np.array([[5, 6, -5], [7, 8, -7]])
axis = 1
arr = np.concatenate((arr1, arr2), axis=axis)
print(f"2D concatenate along axis {axis}: \n{arr}")


# ======================================================================= <<<<<

print()

# ======================================================================= >>>>>
#	Array Join: Stacking
# ======================================================================= >>>>>

'''
Stacking is same as concatenation, the only difference is that stacking 
is done along a new axis.

We can concatenate two 1-D arrays along the second axis which would result 
in putting them one over the other, ie. stacking.

We pass a sequence of arrays that we want to join to the stack() method 
along with the axis. If axis is not explicitly passed it is taken as 0.
'''

arr1 = np.array( [1, 2, 3, 4] )
arr2 = np.array( [5, 6, 7, 8] )
axis = 0
arr = np.stack( ( arr1, arr2 ), axis = axis )
print(f"1D stacking along axis {axis}: \n{arr}")
# Stacking allows you to use the next dimension axis that has not yet been defined.
# The behaviour is a bit hard to predict ... Here it is as if we simply stacked
# along the columns and THEN flip it 90 degrees ...
axis = 1
arr = np.stack( ( arr1, arr2 ), axis = axis )
print(f"1D stacking along axis {axis}: \n{arr}")


# Stacking Along Rows
# NumPy provides a helper function: hstack() to stack along rows.
arr = np.hstack((arr1, arr2))
print(f"Stacking along row axis: \n{arr}")

# NumPy provides a helper function: vstack() to stack along columns.
arr = np.vstack((arr1, arr2))
print(f"Stacking along column axis: \n{arr}")

# Stacking Along Height (depth)
arr = np.dstack((arr1, arr2))
print(f"Stacking along depth: \n{arr}")
# It's as if we are grouping together entries sharing the same index.
print( arr.shape )

# ======================================================================= <<<<<



