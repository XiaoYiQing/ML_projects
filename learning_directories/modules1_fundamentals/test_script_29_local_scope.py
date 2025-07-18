


# ======================================================================= >>>>>
#	Local Scope
# ======================================================================= >>>>>

'''
A variable is only available from inside the region it is created. This is called scope.
'''

#A variable created inside a function is available inside that function:

def myfunc():
  x = 300
  print(x)

myfunc()

# ======================================================================= <<<<<



# ======================================================================= >>>>>
#	Function Inside a Function
# ======================================================================= >>>>>

# The local variable can be accessed from a function within the function:

def myfunc():
  x = 400
  def myinnerfunc():
    print(x)
  myinnerfunc()

myfunc()

# ======================================================================= <<<<<


# ======================================================================= >>>>>
#	Global Scope
# ======================================================================= >>>>>

# A variable created outside of a function is global and can be used by anyone.
x = 500
y = 100
t = 999

def myfunc():
	
	mystr = "[x = %d]" % x
	print( mystr, end = ' ' )
	
	# A global variable is overriden when it is locally defined again.
	y = -100
	mystr = "[y = %d]" % y
	print( mystr, end = ' ')
	
	# A global variable can be defined within local scope using the 'global' keyword
	global z
	z = 777
	
	# You can use the 'global' keyword to also change existing global variables.
	global t
	t = -999
	
myfunc()

mystr = "[z = %d]" % z
print(mystr, end = ' ')

# Locally overidden variables return to original global value once the function exits.
mystr = "[y = %d]" % y
print(mystr, end = ' ')

mystr = "[t = %d]" % t
print(mystr)

# ======================================================================= <<<<<

