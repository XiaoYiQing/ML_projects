


'''
Python does not have built-in support for Arrays, but Python Lists can be used instead.

The examples show you how to use LISTS as ARRAYS, however, to work with arrays in Python 
you will have to import a library, like the NumPy library.
'''

# ======================================================================= >>>>>
#	Arrays
# ======================================================================= >>>>>

# Arrays are used to store multiple values in one single variable.
cars = ["Ford", "Volvo", "BMW"]


# Index access starts at index 0 for the first entry of the array.
x = cars[0]
print(x)

# The length of an array can be obtained using the function len()
x = len(cars)
print(x)

# Looping in an array:
for x in cars:
  print(x, end = ' ')
print()

# Adding entries to an array.
cars.append("Honda")

# Delete the second element of the cars array:
cars.pop(1)

# Delete the element that has the value "Ford":
cars.remove("Ford")
# The list's remove() method only removes the first occurrence of the specified value.


# ======================================================================= <<<<<


