


# ======================================================================= >>>>>
#	JSON
# ======================================================================= >>>>>

'''
JSON is a syntax for storing and exchanging data.
JSON is text, written with JavaScript object notation.
'''

# Python has a built-in package called json, which can be used to work with JSON data.

import json

# If you have a JSON string, you can parse it by using the json.loads() method.
# The result will be a Python dictionary.

# some JSON:
x =  '{ "name":"John", "age":30, "city":"New York" }'

# parse x:
y = json.loads(x)
mystr = 'y is a variable of the class: {}'.format( y.__class__ )
print( mystr )

# the result is a Python dictionary:
mystr = 'name = {}, age = {}'.format(y["name"], y["age"])
print(mystr)

# ======================================================================= <<<<<


# ======================================================================= >>>>>
#	JSON: Python to JSON
# ======================================================================= >>>>>

# a Python object (dict):
x = {
  "name": "John",
  "age": 30,
  "city": "New York"
}

# convert into JSON:
y = json.dumps(x)

# the result is a JSON string:
mystr = 'The y converted to JSON writes as: \n\t{}'.format(y)
print( mystr )

'''
You can convert Python objects of the following types, into JSON strings:

	dict -> Object		list -> Array		tuple -> Array		str -> String
	int -> Number		float -> Number
	True -> true		False -> false
	None -> null	
'''
mystr = 'Dictionary to JSON: {}'.format(json.dumps({"name": "John", "age": 30}))
print(mystr)
mystr = 'List to JSON: {}'.format(json.dumps(["apple", "bananas"]))
print(mystr)
mystr = 'Tuple to JSON: {}'.format(json.dumps(("apple", "bananas")))
print(mystr)
mystr = 'str to JSON: {}'.format(json.dumps(("hello")))
print(mystr)
mystr = 'int to JSON: {}'.format(json.dumps(42))
print(mystr)
mystr = 'float to JSON: {}'.format(json.dumps(31.76))
print(mystr)
mystr = 'True to JSON: {}'.format(json.dumps(True))
print(mystr)
mystr = 'False to JSON: {}'.format(json.dumps(False))
print(mystr)
mystr = 'None to JSON: {}'.format(json.dumps(None))
print(mystr)






# ======================================================================= <<<<<








