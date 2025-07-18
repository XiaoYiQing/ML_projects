




# ======================================================================= >>>>>
#	Dictionary: Copy
# ======================================================================= >>>>>

'''
You cannot copy a dictionary simply by typing dict2 = dict1, because: 
	dict2 will only be a reference to dict1, and changes made in dict1 will automatically also be made in dict2.
'''

# Make a copy of a dictionary with the copy() method:
thisdict = {
  "brand": "Ford",
  "model": "Mustang",
  "year": 1964
}
mydict = thisdict.copy()
thisdict["year"] = 1970
print(thisdict)
print(mydict)

# Another way to make a copy is to use the built-in function dict():
mydict = dict(thisdict)
print(mydict)

# ======================================================================= <<<<<









