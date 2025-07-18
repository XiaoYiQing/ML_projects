


'''
A set is a collection which is 
	unordered
	unchangeable* (Cannot modify items, but can add or remove)
	unindexed
Items also cannot be duplicated. Attempt of duplicates will be ignored and only one instance will be remaining in the set.
'''


# Sets are written with curly brackets.
thisset = {"apple", "banana", "cherry"}
print(thisset)

# Duplicates will be ignored.
thisset = {"apple", "banana", "cherry", "apple"}
print(thisset)

# True and 1 is considered the same value:
thisset = {"apple", "banana", "cherry", True, 1, 2}
print(thisset)
# The values False and 0 are considered the same value in sets, and are treated as duplicates.

# A set can contain different data types:
set1 = {"abc", 34, True, 40, "male"}
print(set1)

# What is the data type of a set? It's 'set'.
myset = {"apple", "banana", "cherry"}
print(type(myset))

# Using the set() constructor to make a set:
thisset = set( ("apple", "banana", "cherry") ) # note the double round-brackets
print(thisset)


