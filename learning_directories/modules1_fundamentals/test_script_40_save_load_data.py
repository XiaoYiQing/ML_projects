

'''
This isn't part of the official tutorials.

This small extra section simply tells you how to save variables to file and later access
them.

The pickle module allows you to do just that.
'''


import os
# Make sure the directory above this current one is visible.
currentdir = os.path.dirname(__file__)

import pickle



# ======================================================================= >>>>>
#	String Formatting: Execute Functions in F-Strings
# ======================================================================= >>>>>

# Define our two test variables, one being simply numbers, the other, letters.
x = [1,2,3,4,5]
y = ["A", "B", "C"]
print( f"x={x}, y={y}" )

# Define the data file name, which is to be located at the same directory as this
# script.
tar_file_name = f"{currentdir}/test_script_40_data.dat"

# Write to file (wb = write to binary).
fw = open( tar_file_name, "wb")
pickle.dump( x, fw )
pickle.dump( y, fw )
fw.close()

x = [2]
y = ["Z"]
print( f"x={x}, y={y}" )

# Load from the data file (rb = Read binary).
fr = open( tar_file_name, "rb" )
x = pickle.load( fr )
y = pickle.load( fr )
fr.close()

print( f"x={x}, y={y}" )

print( "Note how you load data in the same order you dumped them in the file." )

# ======================================================================= <<<<<
