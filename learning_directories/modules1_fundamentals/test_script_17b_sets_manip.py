


'''
You cannot access items in a set by referring to an index or a key.

But you can loop through the set items using a for loop, or ask if a specified value is present in a set, by using the in keyword.
'''

print( 'Loop through a set is random:' )
print( '\t', end = ' ')
# Loop through the set, and print the values:
thisset = {"apple", "banana", "cherry"}
for x in thisset:
  print(x, end = ' ')
print()
# NOTE: the order printed is random.


# You can check if a specific items is or is not in the set
thisset = {"apple", "banana", "cherry"}
print("banana" in thisset)
print("banana" not in thisset)


# ======================================================================= >>>>>
#	Add Items
# ======================================================================= >>>>>

# Add an item to a set, using the add() method:
thisset = {"apple", "banana", "cherry"}
thisset.add("orange")
print(thisset)

# To add items from another set into the current set, use the update() method.
# Add elements from tropical into thisset:
thisset = {"apple", "banana", "cherry"}
tropical = {"pineapple", "mango", "papaya", "banana"}
thisset.update(tropical)
print(thisset)	# Again, duplicates are ignored.

# The object in the update() method does not have to be a set, it can be any iterable object (tuples, lists, dictionaries etc.).
thisset = {"apple", "banana", "cherry"}
mylist = ["kiwi", "orange"]
thisset.update(mylist)
print(thisset)

# ======================================================================= >>>>>
#	Remove Items
# ======================================================================= >>>>>

# Remove "banana" by using the remove() method:
thisset = {"apple", "banana", "cherry"}
thisset.remove("banana")
print(thisset)

# Alternatively, you can use the discard() method, which won't raise an error if the target item does not exist in the set.
thisset = {"apple", "banana", "cherry"}
thisset.discard("banana")
thisset.discard("banana")	# Although "banana" is already discarded, the method won't cause error.
print(thisset)

# You can also discard a random item using pop() method. This is because sets are unordered, and you never know what you discard first.
thisset = {"apple", "banana", "cherry"}
x = thisset.pop()
print(x)
print(thisset)

# The clear() method empties the set.
#	thisset.clear()
# The del keyword will delete the set completely:
#	del thisset





