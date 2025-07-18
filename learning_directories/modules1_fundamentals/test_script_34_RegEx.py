


# ======================================================================= >>>>>
#	RegEx
# ======================================================================= >>>>>

'''
A RegEx, or Regular Expression, is a sequence of characters that forms a search pattern.

RegEx can be used to check if a string contains the specified search pattern.

Python has a built-in package called 're', which can be used to work with Regular Expressions.
'''


import re

# Search the string to see if it starts with "The" and ends with "Spain":
txt = "The rain in Spain"
x = re.search("^The.*Spain$", txt)
print(x)

'''
Many functions are available in the re module. Here are a few:

	findall:	Returns a list containing all matches
	search:		Returns a Match object if there is a match anywhere in the string
	split:		Returns a list where the string has been split at each match
	sub:		Replaces one or many matches with a string
	

The 're' module functions make use of regular expressions to perform matching.
Reg. expr. can be broken down into sub-categories based on what metacharacters are used to identify them:

		[]	A set of characters	"[a-m]"	
	'\'	Signals a special sequence (can also be used to escape special characters)		
	.	Any character (except newline character)	"he..o"	
	^	Starts with	"^hello"	
	$	Ends with	"planet$"	
	*	Zero or more occurrences	"he.*o"	
	+	One or more occurrences	"he.+o"	
	?	Zero or one occurrences	"he.?o"	
	{}	Exactly the specified number of occurrences	"he.{2}o"	
	|	Either or	"falls|stays"	
	()	Capture and group	 

We won't go through every possible expressions.
You will have to look online to get a full presentation of possible regular expressions.
'''

# ======================================================================= <<<<<


# ======================================================================= >>>>>
#	RegEx: Example Cases
# ======================================================================= >>>>>

# The findall() function returns a list containing all matches.
txt = "The rain in Spain"
x = re.findall("ai", txt)
print(x)
# The list contains the matches in the order they are found.
# If no matches are found, an empty list is returned.


# The search() function searches the string for a match, and returns a Match object if there is a match.
# If there is more than one match, only the first occurrence of the match will be returned.
# Search for the first white-space character in the string:
txt = "The rain in Spain"
x = re.search("\\s", txt)
print("The first white-space character is located in position:", x.start())


# The split() function returns a list where the string has been split at each match:
txt = "The rain in Spain"
x = re.split("\\s", txt)
mystr = '"{}" when split with the space char.: {}'.format(txt,x)
print(mystr)
# As can be seen, we can conveniently obtain a list of words from any sentence.

# You can control the number of occurrences by specifying the maxsplit parameter:
txt = "The rain in Spain"
x = re.split("\\s", txt, 1)
mystr = '"{}" when split with the space char. with 1 split maximum: {}'.format(txt,x)
print(mystr)


# The sub() function replaces the matches with the text of your choice:
# Replace every white-space character with the number 12:
txt = "The rain in Spain"
y = "12"
repl_cnt = 2
x = re.sub("\\s", y, txt, repl_cnt)
mystr = '"{}" when the first {} whitespaces are replaced with "{}": {}'.format(txt,repl_cnt,y,x)
print(mystr)


# A Match Object is an object containing information about the search and the result.
# Note: If there is no match, the value None will be returned, instead of the Match Object.
txt = "The rain in Spain"
pattern = "ai"
x = re.search("ai", txt)
mystr = '"{}" when searching for pattern "{}" has the result: \n\t{}'.format(txt,pattern,x)
print(mystr) #this will print an object
'''
The Match object has properties and methods used to retrieve information about the search, and the result:
	.span() returns a tuple containing the start-, and end positions of the match.
	.string returns the string passed into the function
	.group() returns the part of the string where there was a match
'''
x_span = x.span()
x_string = x.string
x_group = x.group()
mystr = 'The search result has [span() = {}][string = {}][group() = {}]'.format( x_span, x_string, x_group )
print(mystr)

# Here is another example:
# Print the position (start- and end-position) of the first match occurrence.
# The regular expression looks for any words that starts with an upper case "S":
txt = "The pain in Spain"
x = re.search(r"\bS\w+", txt)
mystr = '"{}" return the span() when searching any word starting with "S": {}'.format(txt,x.span())
print(mystr)
mystr = '"{}" return the string when searching any word starting with "S": {}'.format(txt,x.string)
print(mystr)
mystr = '"{}" return the group() when searching any word starting with "S": {}'.format(txt,x.group())
print(mystr)

# ======================================================================= <<<<<


