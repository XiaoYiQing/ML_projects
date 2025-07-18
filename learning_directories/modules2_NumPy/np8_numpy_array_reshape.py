



# ======================================================================= >>>>>
#	Array Reshape
# ======================================================================= >>>>>


import numpy as np


# 1D to 2D
arr = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
arr_2D = arr.reshape( 3, 4 )
print( f"{arr} reshaped under dim. (3,4) is: \n{arr_2D}" )


# 1D to 3D
arr_3D = arr.reshape(2, 3, 2)
# print( f"{arr} reshaped under dim. (2,3,2) is: \n{arr_3D}" )


'''
Can We Reshape Into any Shape?
Yes, as long as the elements required for reshaping are equal in both shapes.

We can reshape an 8 elements 1D array into 4 elements in 2 rows 2D array 
but we cannot reshape it into a 3 elements 3 rows 2D array as that would 
require 3x3 = 9 elements.
'''



# Note that reshape returns a view, as the following code shows since the base 
# returned is the original array.
arr = np.array([1, 2, 3, 4, 5, 6, 7, 8])
arr_2D = arr.reshape(2, 4)
print(arr_2D.base)
arr_2D[0,3] = 44
print(arr)

# ======================================================================= <<<<<

print()


# ======================================================================= >>>>>
#	Array Reshape: Unknown Dimension
# ======================================================================= >>>>>

'''
You are allowed to have one "unknown" dimension.

Meaning that you do not have to specify an exact number for one of the 
dimensions in the reshape method.

Pass -1 as the value, and NumPy will calculate this number for you.

Note: We can not pass -1 to more than one dimension.
'''

arr = np.array([1, 2, 3, 4, 5, 6, 7, 8])
newarr = arr.reshape(2, 2, -1)
print(f"The array reshaped under (2, 2, -1) now has shape: {newarr.shape}")


'''
Flattening the arrays
Flattening array means converting a multidimensional array into a 1D array.

We can use reshape(-1) to do this.
'''

arr_v2 = newarr.reshape(-1)
print(f"The reshaped array, now flattened, becomes: \n{arr_v2}")

'''
Note: There are a lot of functions for changing the shapes of arrays in numpy
    flatten
    ravel
There are also functions for rearranging the elements 
    rot90, 
    flip, 
    fliplr, 
    flipud 
    etc. 
These fall under Intermediate to Advanced section of numpy.
'''


# ======================================================================= <<<<<

