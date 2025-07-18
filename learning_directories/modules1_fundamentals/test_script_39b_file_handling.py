

# ======================================================================= >>>>>
#	File Handling: Write
# ======================================================================= >>>>>

# Import the regular expression module.
import re

'''
To write to an existing file, you must add a parameter to the open() function:
	"a" - Append - will append to the end of the file
	"w" - Write - will overwrite any existing content
'''

# Define the full test file
testFileName = "file_handling_test_doc.txt"
keyphrase = "Now the file has more content!"

# First determine if the key phrase is already present in the target file.
f = open( testFileName, "r" )
f_content = f.read()
key_found = bool( re.search( keyphrase, f_content ) )
mystr = f"The keyword is present: {key_found}"
print(mystr)
f.close()

# Add the keyphrase to the target file if it was not present.
if not key_found:
	f = open( testFileName, "a" )
	f.write( "\n" + keyphrase )
	f.close()
	

#open and read the file after the appending:
f = open( testFileName, "r" )
myStr = ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Line by line File Print Start "
print(myStr)
print( f.read() )
myStr = "<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Line by line File Print End "
print(myStr)
f.close()

overwrite_flag = False
if overwrite_flag:
	# the "w" method will overwrite the entire file.
	f = open( testFileName, "w" )
	f.write( "Woops! I have deleted the content!" )
	f.close()
	#open and read the file after the overwriting:
	f = open("demofile3.txt", "r")
	print(f.read())


# ======================================================================= <<<<<


# ======================================================================= >>>>>
#	File Handling: Create/Delete a File
# ======================================================================= >>>>>

'''
To create a new file in Python, use the open() method, with one of the following parameters:
	"x" - Create - will create a file, returns an error if the file exist
	"a" - Append - will create a file if the specified file does not exist
	"w" - Write - will create a file if the specified file does not exist
'''

import os


# Define the dummy test file's name:
testFileName2 = "file_handling_test_doc_tmp.txt"

# Before creating a new file, you should check if it exists already to avoid error in creating a duplicate.
if os.path.exists( testFileName2 ):
	print( "File already exists!" )
else:
	f = open( testFileName2, "x" )
	f.close()



'''
To delete a file, you must import the OS module, and run its os.remove() function.
'''

# Before deleting a file, you should check if it exists already to avoid error in deleting a non-existent file.
if os.path.exists( testFileName2 ):
	os.remove( testFileName2 )
else:
	print("The file does not exist")



# To delete an entire folder, use the os.rmdir() method:
# os.rmdir("myfolder")

# ======================================================================= <<<<<


