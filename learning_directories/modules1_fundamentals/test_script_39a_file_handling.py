


# ======================================================================= >>>>>
#	File Handling
# ======================================================================= >>>>>

'''
Python has several functions for creating, reading, updating, and deleting files.
'''

'''
The key function for working with files in Python is the open() function.
The open() function takes two parameters; filename, and mode.
There are four different methods (modes) for opening a file:

	"r" - Read - Default value. Opens a file for reading, error if the file does not exist
	"a" - Append - Opens a file for appending, creates the file if it does not exist
	"w" - Write - Opens a file for writing, creates the file if it does not exist
	"x" - Create - Creates the specified file, returns an error if the file exists
	
In addition you can specify if the file should be handled as binary or text mode

	"t" - Text - Default value. Text mode
	"b" - Binary - Binary mode (e.g. images)
	
'''

# Define the full test file
testFileName = "file_handling_test_doc.txt"

try:
	# Open the test file for reading (r) and handled in text mode (t), which are the default settings.
	f = open( testFileName )
except:
	# Print error message signaling failure to open target file.
	errStr = f"Could not open the file {testFileName}"
	print( errStr )
# If no error.
else:
	try:
		# Attempt to read the text of the target file.
		fReafContent = f.read()
	except:
		# Print error message signaling failure to read target file.
		errStr = f"Could not read from the file {testFileName}"
		print( errStr )	
	else:
		# Write out the content of the text file, with start and end demarcations:
		myStr = ">>>>> File Content Start >>>>>"
		print(myStr)
		print(fReafContent)
		myStr = "<<<<< File content End <<<<<"
		print(myStr)
	finally:
		f.close()

# I am not going to make such an error for error control from this point on.

# ======================================================================= <<<<<


# ======================================================================= >>>>>
#	File Handling: Selective Reading
# ======================================================================= >>>>>

# By default the read() method returns the whole text, 
# but you can also specify how many characters you want to return:
# Return the 5 first characters of the file:
f = open( testFileName, "r" )
print( f.read(5) )

# The 'f' handler keeps track of where the last character was read, 
# and subsequent partial read functions will read starting from the ealiest unread point.

# You can return one line by using the readline() method:
print( f.readline() )
print( f.readline() )
# Note that reading a line will include the line break special character at the end.
# Printing a read line thus will result in line break, 
#	which is why you see two line breaks when using print() to print.

myStr = ">>>>> Line by line File Print Start >>>>>"
print(myStr)
# You can use f as an iterator to continuously read the lines of the file:
f = open( testFileName, "r")
for x in f:
  print(x)
myStr = "<<<<< Line by line File Print End <<<<<"
print(myStr)


# You should always close your files, in some cases, due to buffering.
#	Changes made to a file may not show until you close the file.
f.close()

# ======================================================================= <<<<<

