

# ======================================================================= >>>>>
#	JSON: Result Formatting
# ======================================================================= >>>>>

import json

print()
# Here is an example of converting a Python object containing all the legal data types:
x = {
  "name": "John",
  "age": 30,
  "married": True,
  "divorced": False,
  "children": ("Ann","Billy"),
  "pets": None,
  "cars": [
    {"model": "BMW 230", "mpg": 27.5},
    {"model": "Ford Edge", "mpg": 24.1}
  ]
}
mystr = 'Collective of all legal data type to JSON: \n{}'.format(json.dumps(x))
print(mystr)
print()


'''
The json.dumps() method has parameters to make it easier to read the result:

	> Use the indent parameter to define the numbers of indents.
	> Use the separators parameter to change the default separator.
		Default value is (", ", ": "), which means using a comma and a space to separate each object, and a colon and a space to separate keys from values.
	> Use the sort_keys parameter to specify if the result should be sorted or not: 
'''

#z = json.dumps(x, indent=4)
z = json.dumps(x, indent=4, separators=(". ", " = "))
#z = json.dumps(x, indent=4, separators=(". ", " = "), sort_keys=True)
mystr = 'Formatted collective of all legal data type to JSON: \n{}'.format(z)
print(mystr)


# ======================================================================= <<<<<
