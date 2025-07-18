





# ======================================================================= >>>>>
#	Access Array Elements
# ======================================================================= >>>>>

import numpy as np

'''
Array indexing is the same as accessing an array element.

You can access an array element by referring to its index number.

The indexes in NumPy arrays start with 0, meaning that the first 
element has index 0, and the second has index 1 etc.
'''
arr = np.array([1, 2, 3, 4])
x = 0
print(f"The entry of ndarray at index {[x]} is: {arr[x]}")


'''
To access elements from 2-D arrays we can use comma separated integers 
representing the dimension and the index of the element.

Think of 2-D arrays like a table with rows and columns, where the dimension 
represents the row and the index represents the column.
'''
arr = np.array([[1,2,3,4,5], [6,7,8,9,10]])

z0 = 0
z1 = 1
print(f"The entry of ndarray at index [{z0},{z1}] is: {arr[z0,z1]}")


'''
To access elements from 3-D arrays we can use comma separated integers 
representing the dimensions and the index of the element.
'''
arr = np.array([[[1, 2, 3], [4, 5, 6]], [[7, 8, 9], [10, 11, 12]]])

z0 = 0
z1 = 1
z2 = 2
print(f"The entry of ndarray at index [{z0},{z1},{z2}] is: {arr[z0,z1,z2]}")

# Result should be 6
# Explanation: indices reading order follows the wrapping order from outer layer to 
#   inner layer of the array:
#   Start:    [[[1, 2, 3], [4, 5, 6]], [[7, 8, 9], [10, 11, 12]]]
#   z0 = 0 -> [[1, 2, 3], [4, 5, 6]]
#   z1 = 1 -> [4, 5, 6]
#   z2 = 2 -> [6]


'''
Negative Indexing
Use negative indexing to access an array from the end.
'''

arr = np.array([[1,2,3,4,5], [6,7,8,9,10]])
print('Last element from 2nd dim: ', arr[1, -1])
#   Start:    [[1,2,3,4,5], [6,7,8,9,10]]
#   z0 = 1 -> [6,7,8,9,10]
#   z1 = -1 -> [10]


# ======================================================================= <<<<<


