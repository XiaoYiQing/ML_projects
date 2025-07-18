



'''
You can search an array for a certain value, and return the indexes that 
get a match.
'''


# ======================================================================= >>>>>
#	Searching Arrays
# ======================================================================= >>>>>

import numpy as np

arr = np.array([1, 2, 3, 4, 5, 4, 4])
print(f"Array is: {arr}")

x = np.where(arr == 4)
print(f"Indexes where 4 appears in the array: {x[0]}")

# Find the indexes where the values are even:
x = np.where(arr%2 == 0)
print(f"Indexes of even values in the array: {x[0]}")

# Find the indexes where the values are even:
x = np.where(arr%2 == 1)
print(f"Indexes of odd values in the array: {x[0]}")

# ======================================================================= <<<<<

print()

# ======================================================================= >>>>>
#	Searching Arrays: Search Sorted
# ======================================================================= >>>>>

'''
There is a method called searchsorted() which performs a binary search 
in the array, and returns the index where the specified value would be 
inserted to maintain the search order.

The searchsorted() method is assumed to be used on sorted arrays.

The method starts the search from the left and returns the first index where 
the number 7 is no longer larger than the next value.
'''


arr = np.array([6, 7, 8, 9])
print(f"Array is: {arr}")

# Perform binary search.
x = np.searchsorted(arr, 7)
print(f"7 should be placed at index {x} to maintain sorted order.")

'''
Search From the Right Side
By default the left most index is returned, but we can give side='right' to 
return the right most index instead.

The method starts the search from the right and returns the first index where 
the number 7 is no longer less than the next value.
'''

x = np.searchsorted(arr, 7, side='right')
print(f"7 should be placed at index {x} to maintain sorted order.")

# ======================================================================= <<<<<

print()

# ======================================================================= >>>>>
#	Searching Arrays: Multiple Values
# ======================================================================= >>>>>

'''
To search for more than one value, use an array with the specified values.
'''

arr = np.array([1, 3, 5, 7])
print(f"Array is: {arr}")
x = np.searchsorted(arr, [2, 4, 6])
print(f"[2,4,6] should be placed at indices {x}, respectively, to maintain sorted order.")
# Find the indexes where the value 7 should be inserted, starting from the right.

# ======================================================================= <<<<<

