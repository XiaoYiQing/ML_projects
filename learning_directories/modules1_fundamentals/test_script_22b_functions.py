


# ======================================================================= >>>>>
#	Functions: Default Parameter
# ======================================================================= >>>>>

# If we call the function without argument, it uses the default value:
def my_function(country = "Norway"):
  print("I am from " + country)

my_function("Sweden")
my_function()

# ======================================================================= <<<<<



# ======================================================================= >>>>>
#	Functions: Passing a List as an Argument
# ======================================================================= >>>>>

# You can send any data types as the argument to a function (string, number, list, dictionary etc.), 
# and it will be treated as the same data type inside the function.
# E.g. if you send a List as an argument, it will still be a List when it reaches the function:
def my_function(food):
	for x in food:
		print(x, end = ' ')
	print()

fruits = ["apple", "banana", "cherry"]

my_function(fruits)

# ======================================================================= <<<<<


# ======================================================================= >>>>>
#	Functions: Return
# ======================================================================= >>>>>

# To let a function return a value, use the return statement:
def my_function(x):
  return 5 * x

returned_val = my_function(3)
print(returned_val)

# ======================================================================= <<<<<


# ======================================================================= >>>>>
#	Functions: Positional-Only and Keyword-Only Arguments
# ======================================================================= >>>>>

# You can specify that a function can have ONLY positional arguments.
# To specify that a function can have only positional arguments, add , / after the arguments:
def my_function(x, /):
  print(x)
my_function(3)
# Note that the following function call would trigger error.
#	my_function( x = 3 )


# To specify that a function can have only keyword arguments, add *, before the arguments:
def my_function(*, x):
  print(x)
my_function(x = 4)
# Note that the following function call would trigger error.
#	my_function(4)


# You can combine the two argument types in the same function.
# Any argument before the / , are positional-only, and any argument after the *, are keyword-only.
def my_function(a, b, /, *, c, d):
  print(a + b + c + d)
my_function(5, 6, c = 7, d = 8)


# ======================================================================= <<<<<






