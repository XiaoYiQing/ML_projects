


# ======================================================================= >>>>>
#	PIP
# ======================================================================= >>>>>

'''
PIP is a package manager for Python packages, or modules if you like.
	-> A package contains all the files you need for a module.
		-> Modules are Python code libraries you can include in your project.
		
If you have Python version 3.4 or later, PIP is included by default.
	We shall assume that we have version 3.4 or later.
'''

'''
For this example/exercise, we are to install the package called 'camelcase'.
To do so, open your command prompt and perform the following steps:
	1- Navigate your command prompt to the location of Python's script directory.
		To determine the python script directory, use the sys.path[0] command:
			import sys
			print( sys.path[0] )
	2- With your command prompt at the python script directory:
		C:\\your_python_script_dir>pip install camelcase
'''

# Here is an example of the use of the package/module 'camelcase':
import camelcase
c = camelcase.CamelCase()
txt = "hello world"

mystr = '{} -> CamelCase ->{}'.format( txt, c.hump(txt) )

print(mystr)


'''
You can find further packages at https://pypi.org/.

If you want to uninstall a package, say the 'camelcase' package, you can write the following
command in the command prompt at the Python's script directory:
	C:\\your_python_script_dir>pip uninstall camelcase
	
To view the list of packages installed on your system, you can write the following
command in the command prompt at the Python's script directory:
	C:\\your_python_script_dir>pip list
'''


# ======================================================================= <<<<<


