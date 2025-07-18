

'''
List comprehension offers a shorter syntax when you want to create a new list 
based on the values of an existing list.

The syntax goes as follow:
	newlist = [expression for item in iterable if condition == True]
	
condition: 
	Filter that only accepts the items that valuate to True.
	It is entirely optional 
	
iterable:
	An iterable object, such as a list, tuple, set, etc.
	
expression:
	The current item in the iteration, but it is also the outcome, which you can manipulate before it ends up like a list item in the new list.
	
item:
	The temporary variable for storing the current item in the iterable at the current loop index.
	You simply define it and do not directly change it. You can use it in the expression.
'''


# Let's start with a simple numerical example:
numArr = range(10)
strArr = [ "Apple", "Orange", "Banana" ];

# Simple shorthand for creating the same array.
newlist = [x for x in numArr]
print(newlist)
# Simple use of condition:
newlist = [x for x in numArr if x > 4]
print(newlist)
# Simple use of manipulation on the expression:
newlist = [x+1 for x in numArr if x > 4]
print(newlist)
# You can outright ignore the item in the expression:
newlist = [-1 for x in numArr if x > 4]
print(newlist)

print()

# Simple string based example.
newlist = [x for x in strArr]
print(newlist)
# String example with condition
newlist = [x for x in strArr if "e" in x]
print(newlist)
# The expression itself can have a conditon, but it doesn't act as a filter, but as a way to manipulate the outcome.
newlist = [x if "n" in x else x.upper() for x in strArr if "e" in x]
print(newlist)
