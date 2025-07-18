


# ======================================================================= >>>>>
#	Modules
# ======================================================================= >>>>>

'''
Consider a module to be the same as a code library.

A file containing a set of functions you want to include in your application.
'''


import mymodule

# When using a function from a module, use the syntax: module_name.function_name.
mymodule.greeting("Jonathan")

# When accessing variables from amodule, use the syntax: module_name.variable_name.
a = mymodule.person1

mystr = "[age = %d]" % a["age"]
print( mystr )

# You can selectively import parts of the module by using the 'from' keyword:
from mymodule import person1 as mx_person
mystr = "[name = %s]" % mx_person["name"]
print( mystr )
# Note: When importing using the from keyword, do not use the module name when referring to elements in the module. Example: mx_person["age"]

# ======================================================================= <<<<<


# ======================================================================= >>>>>
#	Modules: Alias
# ======================================================================= >>>>>

# The imported module may be renamed under a different alias:
import mymodule as mx

mx.greeting("Jonathan")

# ======================================================================= <<<<<


# ======================================================================= >>>>>
#	Modules: Built-in Modules
# ======================================================================= >>>>>

# There are several built-in modules in Python, which you can import whenever you like.
import platform

x = platform.system()
print(x)

# There is a built-in function to list all the function names (or variable names) in a module. 
# The dir() function:
mx_fct_list = dir(platform)
#print(mx_fct_list)
# The dir() function can be used on all modules, also the ones you create yourself.

# ======================================================================= <<<<<



