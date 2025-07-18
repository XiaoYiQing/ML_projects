


# ======================================================================= >>>>>
#	Dictionary: Access
# ======================================================================= >>>>>

# You can access the items of a dictionary by referring to its key name, inside square brackets:
thisdict = {
  "brand": "Ford",
  "model": "Mustang",
  "year": 1964
}
x = thisdict["model"]
print(x)

# Alternatively, you can use the method get()
x = thisdict.get("model")

# To specifically obtain the keys of the dictionary, use the keys() method:
keys_list = thisdict.keys()
print( keys_list )

# 'keys_list' is a special list that specifically reflects the keys of the parent object.
# Changing the keys of the parent also changes the key list object.
thisdict["color"] = "white"
print( keys_list )

# To specifically obtain the values of the dictionary, use the values() method:
values_list = thisdict.values()
print( values_list )

# The list of the values is a view of the dictionary, meaning that any changes done to the dictionary will be reflected in the values list.
thisdict["year"] = 2020
print( values_list )

# The items() method will return each item in a dictionary, as tuples in a list.
x = thisdict.items()
print(x)
# The returned list is a view of the items of the dictionary, meaning that any changes done to the dictionary will be reflected in the items list.
thisdict["year"] = 2024
print(x)


# ======================================================================= <<<<<










