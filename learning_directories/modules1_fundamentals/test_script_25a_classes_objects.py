


'''
Almost everything in Python is an object, with its properties and methods.

A Class is like an object constructor, or a "blueprint" for creating objects.
'''


# ======================================================================= >>>>>
#	Classes/Objects
# ======================================================================= >>>>>

# To create a class, use the keyword class:
class MyClass:
  x = 5


# Now we can use the class named MyClass to create objects:
p1 = MyClass()
print(p1.x)

# ======================================================================= <<<<<


# ======================================================================= >>>>>
#	Classes: __init__() Function
# ======================================================================= >>>>>

'''
The examples above are classes and objects in their simplest form, and are not 
really useful in real life applications.

To understand the meaning of classes we have to understand the built-in __init__() 
function.

All classes have a function called __init__(), which is always executed when the 
class is being initiated.

Use the __init__() function to assign values to object properties, or other 
operations that are necessary to do when the object is being created:
'''

# Create a class called 'Person' and specify the constructor function's content:
class Person:
  def __init__(self, name, age):
    self.name = name
    self.age = age
'''
Note: The self parameter is a reference to the current instance of the class, and is used to access variables that belong to the class.
It does not have to be named self , you can call it whatever you like, but it has to be the first parameter of any function in the class.
'''

# Define an object instance under the class 'Person' with the expected arguments to the constructor.
p1 = Person( "John", 36 )

print( p1.name, end = ' ' )
print( p1.age )

# ======================================================================= <<<<<


# ======================================================================= >>>>>
#	Classes: __str__() Function
# ======================================================================= >>>>>

# The __str__() function controls what should be returned when the class object is represented as a string.
# If not set, is not set, the string representation of the object is returned:
print(p1)
# Not a very informative string,but it does tell you the exact location of the object ...


class Person:
	def __init__(self, name, age):
		self.name = name
		self.age = age

	def __str__(self):
		return f"{self.name}({self.age})"

p1 = Person("John", 36)

print(p1)

# ======================================================================= <<<<<


# ======================================================================= >>>>>
#	Classes: Object Methods
# ======================================================================= >>>>>

# Objects can also contain methods. Methods in objects are functions that belong to the object.
class Person:
	def __init__(self, name, age):
		self.name = name
		self.age = age

	def __str__(self):
		return f"{self.name}({self.age})"

	def myfunc(self):
		print("Hello my name is " + self.name)

p1 = Person("John", 36)
p1.myfunc()

# ======================================================================= <<<<<



# ======================================================================= >>>>>
#	Classes: Delete Object and Object Properties
# ======================================================================= >>>>>
# You can delete specific attributes of the object. 
# Doing so means the object no longer has the attribute, and accessing it would result in error.
del p1.age
# The following print statement would generate an error since the 'age' attribute no longer exsts in 'p1' object.
#	print(p1)


# You can straight up delete the object too.
del p1
# ======================================================================= <<<<<


# ======================================================================= >>>>>
#	Classes: Pass Statement
# ======================================================================= >>>>>

# If for some reason you need an empty class, you can use the pass statement.
class Person:
  pass

# ======================================================================= <<<<<



