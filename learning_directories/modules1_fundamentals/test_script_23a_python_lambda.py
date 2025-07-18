

'''
A lambda function is a small anonymous function.
A lambda function can take any number of arguments, but can only have one expression.
A Lambda function follows the structure:
	lambda arguments : expression
	
Use lambda functions when an anonymous function is required for a short period of time.
'''

# ======================================================================= >>>>>
#	Lambda Function
# ======================================================================= >>>>>

# A simple example of lambda function:
x = lambda a, b : a * b
print(x(5, 6))

# ======================================================================= <<<<<



# ======================================================================= >>>>>
#	Lambda Function
# ======================================================================= >>>>>

'''
The power of lambda is better shown when you use them as an anonymous function inside another function.

This is possible due to the fact that a lambda function is defined over a single line.
'''

# Say you have a function definition that takes one argument, and that argument will be multiplied with an unknown number:
def myfunc(n):
  return lambda a : a * n

# The above function returns the handler of a lambda function (A function producing a function).
# Use that function definition to make a function that always doubles the number you send in:
my_doubler_func = myfunc(2)

print( my_doubler_func(11) )

# ======================================================================= <<<<<











