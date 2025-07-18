

# True or false variables.




print(10 > 9)
print(10 < 9)
print( )

# Most variables convert to true if evaluated as a boolean, with the zero digit being the exception.
x = "\'Hello\' is {}"
y = x.format( bool( "Hello" ) )
print(y)
x = "\'15\' is {}"
y = x.format( bool( 15 ) )
print(y)
x = "\'0\' is {}"
y = x.format( bool( 0 ) )
print(y)

# Empty sets also evaluate to false. This is due to the fact that the default logic of the bool function is to seek the 'length' of the variable, which is only 0 if the set is empty or the variable is null.
myAns = "\'False\' is {0}, \'None\' is {1}, "
myAns = myAns + "\'\"\"\' is {2}, \'()\' is {3}, "
myAns = myAns + "\'[]\' is {4}, \'{{}}\' is {5}"
myAns = myAns.format( bool(False), bool(None), bool(""), bool(()), bool([]), bool({}) )
print( myAns )


# One more value, or object in this case, evaluates to False, and that is if you have an object that is made from a class with a __len__ function that returns 0 or False:
class myclass():
  def __len__(self):
    return 0

myobj = myclass()
print(bool(myobj))









