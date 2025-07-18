


# Define a global variable (which is simply defining a variable outside a function definition).
x = "awesome"

def myfunc():
	print( "Chocolate is " + x + "\n" )
	
myfunc()


# Local variable sharing the same name as the global variable overwrites it within the function, but not outside the function.
def myfunc2():
	x = "Terrible"
	print( "Chocolate is " + x )

myfunc2()
print( "Chocolate is " + x + "\n" )



# Global variable can be created inside a function with the 'global' keyword.
def myfunc3():
	global y
	y = "Crazy"
	
	# You can also modify existing global variables within a function.
	global x
	x = "Terrific"
	
myfunc3()
print( "Chocolate is " + y + " " + x )
