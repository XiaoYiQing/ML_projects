


'''
Tuples are used to store multiple items in a single variable.

A tuple is a collection which is ordered and unchangeable.

Tuples are written with round brackets.

Tuple items are ordered, unchangeable, and allow duplicate values.
	> When we say that tuples are ordered, it means that the items have a defined order, and that order will not change.
	> Tuples are unchangeable, meaning that we cannot change, add or remove items after the tuple has been created.
	> Since tuples are indexed, they can have items with the same value:
	
Tuple items are indexed, the first item has index [0], the second item has index [1] etc.
'''


thistuple = ("apple", "banana", "cherry")
print(thistuple)

# To create a tuple with only one item, you have to add a comma after the item, otherwise Python will not recognize it as a tuple.
thistuple = ("apple",)
print(type(thistuple))
#NOT a tuple
thistuple = ("apple")
print(type(thistuple))



# A tuple can contain different data types:
tuple1 = ("abc", 34, True, 40, "male")





