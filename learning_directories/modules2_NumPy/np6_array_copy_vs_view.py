


'''
The Difference Between Copy and View
The main difference between a copy and a view of an array is that the copy 
is a new array, and the view is just a view of the original array.

The copy owns the data and any changes made to the copy will not affect 
original array, and any changes made to the original array will not affect 
the copy.

The view does not own the data and any changes made to the view will affect 
the original array, and any changes made to the original array will affect 
the view.
'''


# ======================================================================= >>>>>
#	Array Copy and View
# ======================================================================= >>>>>

import numpy as np


arr = np.array([1, 2, 3, 4, 5])
x = arr.copy()
y = arr.view()
arr[0] = 42
print( "Changing copy with x[0] = 42:" )
print(f"Original array: {arr}")
print(f"Copy of array: {x}")
print(f"view of array: {y}")

# The view is expected to be affected by the changes made to the original array.

y[2] = 99
print( "Changing view with y[2] = 99:" )
print(f"Original array: {arr}")
print(f"Copy of array: {x}")
print(f"view of array: {y}")

# The original array SHOULD be affected by the changes made to the view.


'''
Check if Array Owns its Data.

As mentioned above, copies owns the data, and views does not own the data, 
but how can we check this?
Every NumPy array has the attribute base that returns None if the array 
owns the data.
Otherwise, the base  attribute refers to the original object.
'''
print()
print(f"The base of the copy is: {x.base}")
print(f"The base of the view is: {y.base}")
# The copy returns None.
# The view returns the original array.

# ======================================================================= <<<<<