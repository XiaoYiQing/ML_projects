



# ======================================================================= >>>>>
#	Dictionary: Nested
# ======================================================================= >>>>>

# A dictionary can contain dictionaries, this is called nested dictionaries.
myfamily = {
  "child1" : {
    "name" : "Emil",
    "year" : 2004,
  },
  "child2" : {
    "name" : "Tobias",
    "year" : 2007,
  },
  "child3" : {
    "name" : "Linus",
    "year" : 2011,
	"sex"  : "m"
  }
}
print( myfamily )

# Or, if you want to add three dictionaries into a new dictionary.
# Create three dictionaries, then create one dictionary that will contain the other three dictionaries:
child1 = {
  "name" : "Emil",
  "year" : 2004
}
child2 = {
  "name" : "Tobias",
  "year" : 2007
}
child3 = {
  "name" : "Linus",
  "year" : 2011,
  "sex"  : "m"
}

myfamily = {
  "child1" : child1,
  "child2" : child2,
  "child3" : child3
}
print( myfamily )

# ======================================================================= <<<<<


# ======================================================================= >>>>>
#	Dictionary: Nested Dictionary Access
# ======================================================================= >>>>>

# To access items from a nested dictionary, you use the name of the dictionaries, starting with the outer dictionary:
print( myfamily["child2"]["name"] )

# You can loop through a dictionary by using the items() method.
# Loop through the keys and values of all nested dictionaries:
for x, obj in myfamily.items():
  print(x)

  for y in obj:
    print( y + ':', obj[y] )
# ======================================================================= <<<<<


