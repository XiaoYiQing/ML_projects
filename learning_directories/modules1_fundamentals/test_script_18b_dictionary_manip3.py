


# ======================================================================= >>>>>
#	Dictionary: Loop
# ======================================================================= >>>>>

# You can loop through a dictionary by using a for loop.

# When looping through a dictionary, the return value are the keys of the dictionary, but there are methods to return the values as well.
thisdict = {
  "brand": "Ford",
  "model": "Mustang",
  "year": 1964
}
for x in thisdict:
  print( x, end = ' ' )
print()
# Print all values in the dictionary, one by one:
for x in thisdict:
  print( thisdict[x], end = ' ' )
print()


# You can directly loop through the values of the dictionary using the values() method:
for x in thisdict.values():
  print( x, end = ' ' )
print()

# You can use the keys() method to return the keys of a dictionary:
for x in thisdict.keys():
  print( x, end = ' ' )
print()

# Loop through both keys and values, by using the items() method:
for x, y in thisdict.items():
  print( '[', x, ':', y, ']', end = ' ' )
print()

# ======================================================================= <<<<<



