



# ======================================================================= >>>>>
#	Functions
# ======================================================================= >>>>>

# A function is a block of code which only runs when it is called.
# You can pass data, known as parameters, into a function.
# A function can return data as a result.

# In Python a function is defined using the def keyword:
def my_function( arg1 ):
  print( "This function prints the input argument, which is: " + arg1 )

my_function( 'Large' )


# By default, a function must be called with the correct number of arguments. 
# Meaning that if your function expects 2 arguments, 
#	you have to call the function with 2 arguments, not more, and not less.
def my_function(fname, lname):
  print(fname + " " + lname)

my_function("Emil", "Refsnes")
# If you try to call the function with 1 or 3 arguments, you will get an error.


# function definitions cannot be empty, but if you for some reason have a function definition with no content, put in the pass statement to avoid getting an error.
def myfunction():
  pass

# ======================================================================= <<<<<



# ======================================================================= >>>>>
#	Functions: Variable Number of Arguments
# ======================================================================= >>>>>

# If you do not know how many arguments that will be passed into your function, 
# add a * before the parameter name in the function definition.
# This way the function will receive a tuple of arguments, and can access the items accordingly:
def my_function(*kids):
	print( kids.__class__ )
	print( "The youngest child is " + kids[2] )

my_function( "Emil", "Tobias", "Linus" )

# ======================================================================= <<<<<


# ======================================================================= >>>>>
#	Functions: Variable Number of Arguments
# ======================================================================= >>>>>

# You can also send arguments with the key = value syntax.
# This way the order of the arguments is hardset and order of specification does not matter.

def my_function(child3, child2, child1):
  print("The youngest child is " + child3)

my_function(child2 = "Emil", child1 = "Tobias", child3 = "Linus")


# Arbitrary Keyword Arguments, **kwargs
# If you do not know how many keyword arguments that will be passed into your function, add two asterisk: ** before the parameter name in the function definition.
# This way the function will receive a dictionary of arguments, and can access the items accordingly:
def my_function(**kid):
  print("His last name is " + kid["lname"] + ". His first name is " + kid["fname"])

my_function(fname = "Tobias", lname = "Refsnes")

# ======================================================================= <<<<<




