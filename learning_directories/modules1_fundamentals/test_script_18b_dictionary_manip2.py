


# ======================================================================= >>>>>
#	Dictionary: Change Values
# ======================================================================= >>>>>

# Dicrect change of target key's value.
thisdict = {
  "brand": "Ford",
  "model": "Mustang",
  "year": 1964
}
print(thisdict)
thisdict["year"] = 2018
print(thisdict)


# The update() method will update the dictionary with the items from the given argument.
# The argument must be a dictionary, or an iterable object with key:value pairs.
thisdict.update({"year": 2020})
print(thisdict)

# ======================================================================= <<<<<


# ======================================================================= >>>>>
#	Dictionary: Adding Items
# ======================================================================= >>>>>

# Adding an item to the dictionary is done by using a new index key and assigning a value to it:
thisdict["color"] = "red"
print(thisdict)

# The update() method will update the dictionary with the items from a given argument. If the item does not exist, the item will be added.
# The argument must be a dictionary, or an iterable object with key:value pairs.
thisdict.update( {"width (m)": 4.5} )
print(thisdict)

# ======================================================================= <<<<<


# ======================================================================= >>>>>
#	Dictionary: Removing Items
# ======================================================================= >>>>>
# The pop() method removes the item with the specified key name:
thisdict.pop("model")
print(thisdict)

# The popitem() method removes the last inserted item (in versions before 3.7, a random item is removed instead):
thisdict.popitem()
print(thisdict)

# The del keyword removes the item with the specified key name:
del thisdict["year"]
print(thisdict)

# The clear() method empties the dictionary:
thisdict.clear()
print(thisdict)

#The del keyword can also delete the dictionary completely:
del thisdict
# ======================================================================= <<<<<








