


'''
Sorting means putting elements in an ordered sequence.

Ordered sequence is any sequence that has an order corresponding to elements, 
like numeric or alphabetical, ascending or descending.
'''


# ======================================================================= >>>>>
#	Sorting Arrays
# ======================================================================= >>>>>

'''
The NumPy ndarray object has a function called sort(), that will sort a 
specified array.

This method returns a copy of the array, leaving the original array unchanged.
'''
import numpy as np

arr = np.array([3, 2, 0, 1])
print(f"The original array: {arr}")
arr_sorted = np.sort(arr)
print(f"The sorted array: {arr_sorted}")

# You can sort arrays of strings, or any other data type:
arr = np.array(['banana', 'cherry', 'apple'])
print(f"The original array: {arr}")
arr_sorted = np.sort(arr)
print(f"The sorted array: {arr_sorted}")

# You can sort boolean arrays.
arr = np.array([True, False, True])
print(f"The original array: {arr}")
arr_sorted = np.sort(arr)
print(f"The sorted array: {arr_sorted}")

# ======================================================================= <<<<<


# ======================================================================= >>>>>
#	Sorting Arrays: 2D-Arrays
# ======================================================================= >>>>>

'''
If you use the sort() method on a 2-D array, sub-arrays will be sorted.
'''

arr = np.array([[9, 8, 7], [5, 6, 4],[3, 2, 1]])
print(f"The original array: \n{arr}")
arr_sorted = np.sort(arr)
print(f"The sorted array: \n{arr_sorted}")

# ======================================================================= <<<<<
