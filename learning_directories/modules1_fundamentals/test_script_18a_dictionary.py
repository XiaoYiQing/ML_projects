


'''
Dictionaries are used to store data values in key:value pairs.

A dictionary is a collection which is ordered* (as of python 3.7), 
changeable and do not allow duplicates.
'''


# Dictionaries are written with curly brackets, and have keys and values:
# Create and print a dictionary:
thisdict = {
  "brand": "Ford",
  "model": "Mustang",
  "year": 1964
}
print(thisdict)


# Duplicate keys cannot exist (last duplicate instance overwirtes all previous), though duplicate values can happen:
thisdict = {
  "brand": "Ford",
  "model": "Mustang",
  "year": 1964,
  "year": 2020,
  "lol": "Mustang"
}
print(thisdict)


# The length of a dictionary is the number of key-value pairs:
print(len(thisdict))


# The values in dictionary items can be of any data type:
thisdict = {
  "brand": "Ford",
  "electric": False,
  "year": 1964,
  "colors": ["red", "white", "blue"]
}

# The dictionaries are defined as objects with the data type 'dict'.
print(type(thisdict))

# A more formal way of defining a dictionary is through its constructor:
thisdict = dict(name = "John", age = 36, country = "Norway")
print(thisdict)




