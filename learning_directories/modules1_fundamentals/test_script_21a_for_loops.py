


# ======================================================================= >>>>>
#	For Loops
# ======================================================================= >>>>>

# A for loop is used for iterating over a sequence 
#	(that is either a list, a tuple, a dictionary, a set, or a string).
fruits = ["apple", "banana", "cherry"]
for x in fruits:
  print( x, end = ' ' )
print()

# Even strings are iterable objects, they contain a sequence of characters:
for x in "banana":
  print( x, end = ' ' )
print()

# With the break statement we can stop the loop before it has looped through all the items:
fruits = ["apple", "banana", "cherry"]
for x in fruits:
  print( x, end = ' ' )
  if x == "banana":
    break
print()

# With the continue statement we can stop the current iteration of the loop, and continue with the next:
fruits = ["apple", "banana", "cherry"]
for x in fruits:
  if x == "banana":
    continue
  print( x, end = ' ' )
print()


# To loop through a set of code a specified number of times, we can use the range() function,
# The range() function returns a sequence of numbers, starting from 0 by default, and increments by 1 (by default), and ends at a specified number.
for x in range(6):
  print( x, end = ' ' )
print()
# Note that range(6) is not the values of 0 to 6, but the values 0 to 5.


# The range() function defaults to 0 as a starting value, however it is possible to specify the starting value by adding a parameter: range(2, 6), which means values from 2 to 6 (but not including 6):
for x in range(2, 6):
  print( x, end = ' ' )
print()


# The range() function defaults to increment the sequence by 1, however it is possible to specify the increment value by adding a third parameter: range(2, 30, 3):
for x in range(2, 30, 3):
  print( x, end = ' ' )
print()


# ======================================================================= <<<<<










