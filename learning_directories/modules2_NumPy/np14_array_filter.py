


'''
Filtering Arrays
Getting some elements out of an existing array and creating a new array out 
of them is called filtering.

In NumPy, you filter an array using a boolean index list.

If the value at an index is True that element is contained in the filtered array, 
if the value at that index is False that element is excluded from the filtered array.
'''


# ======================================================================= >>>>>
#	Array Filter
# ======================================================================= >>>>>

import numpy as np

arr = np.array([41, 42, 43, 44])
print(f"The original array: {arr}")

x = [True, False, True, False]
print(f"The boolean array: {x}")
newarr = arr[x]
print(f"The filtered array: {newarr}")

# ======================================================================= <<<<<

print()

# ======================================================================= >>>>>
#	Array Filter: Creating Filter
# ======================================================================= >>>>>

'''
Creating the Filter Array:
In the example above we hard-coded the True and False values, but the 
common use is to create a filter array based on conditions.
'''
# Create an empty list
filter_arr = []

# go through each element in arr
for element in arr:
  # if the element is higher than 42, set the value to True, otherwise False:
  if element > 42:
    filter_arr.append(True)
  else:
    filter_arr.append(False)

print(f"The filter array (> 42): {filter_arr}")
newarr = arr[filter_arr]
print(f"The filtered array: {newarr}")



print()
# Create a filter array that will return only even elements from the 
# original array:
arr = np.array([1, 2, 3, 4, 5, 6, 7])
print(f"The original array: {arr}")

# Create an empty list
filter_arr = []

# go through each element in arr
for element in arr:
  # if the element is completely divisble by 2, set the value to True, otherwise False
  if element % 2 == 0:
    filter_arr.append(True)
  else:
    filter_arr.append(False)

print(f"The filter array (even number): {filter_arr}")
newarr = arr[filter_arr]
print(f"The filtered array: {newarr}")

# ======================================================================= <<<<<

print()

# ======================================================================= >>>>>
#	Array Filter: Directly From Array
# ======================================================================= >>>>>

arr = np.array([41, 42, 43, 44])
print(f"The original array: {arr}")

filter_arr = arr > 42
print(f"The filter array (> 42): {filter_arr}")
newarr = arr[filter_arr]
print(f"The filtered array: {newarr}")

filter_arr = arr % 2 == 0
print(f"The filter array (even number): {filter_arr}")
newarr = arr[filter_arr]
print(f"The filtered array: {newarr}")

# ======================================================================= <<<<<


