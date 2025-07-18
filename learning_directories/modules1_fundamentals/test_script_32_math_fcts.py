



# ======================================================================= >>>>>
#	Math Functions
# ======================================================================= >>>>>

'''
Python has a set of built-in math functions, including an extensive math module, that allows you to perform mathematical tasks on numbers.
'''


# The min() and max() functions can be used to find the lowest or highest value in an iterable:
myNumList = [ 5, 10, 25 ]
x = min( myNumList )
y = max( myNumList )

mystr = "[max = %d, min = %d]" % (x, y)
print(mystr)

# The abs() function returns the absolute (positive) value of the specified number:
x = -7.25
y = abs(x)
mystr = "[abs(%d) = %d]" % (x, y)
print(mystr)

# The pow(x, y) function returns the value of x to the power of y (x^y).
x = [ 4, 3 ]
y = pow(x[0], x[1])
mystr = "[pow(%d,%d) = %d]" % (x[0], x[1], y)
print(mystr)

# ======================================================================= <<<<<


# ======================================================================= >>>>>
#	Math Functions: Math Module
# ======================================================================= >>>>>

# Python has also a built-in module called math, which extends the list of mathematical functions.

# To use it, you must import the math module:

import math

# The math.sqrt() method for example, returns the square root of a number:
x = 62
y = math.sqrt(x)
mystr = "[math.sqrt(%d) = %f]" % (x, y)
print(mystr)

# The math.pi constant, returns the value of PI (3.14...):
x = math.pi
mystr = 'math.pi = {}'.format(x)
print(mystr)


'''
There are many more functions from the math module that are useful which you can find in references online.
'''
# ======================================================================= <<<<<





