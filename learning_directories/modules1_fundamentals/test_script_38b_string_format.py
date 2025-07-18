


# ======================================================================= >>>>>
#	String Formatting: Execute Functions in F-Strings
# ======================================================================= >>>>>

# You can execute functions inside the placeholder.
# Use the string method upper()to convert a value into upper case letters:
fruit = "apples"
txt = f"I love {fruit.upper()}"
print(txt)

# The function does not have to be a built-in Python method, you can create your own functions and use them:
def myconverter(x):
  return x * 0.3048
txt = f"The plane is flying at a {myconverter(30000)} meter altitude"
print(txt)

# ======================================================================= <<<<<



# ======================================================================= >>>>>
#	String Formatting: More Modifiers
# ======================================================================= >>>>>

# At the beginning of this chapter we explained how to use the .2f modifier to format a number into a fixed point number with 2 decimals.
# There are several other modifiers that can be used to format values:

# Use a comma as a thousand separator:
price = 59000
txt = f"The price is {price:,} dollars"
print(txt)

'''
Here is a list of all the formatting types:

:<		Left aligns the result (within the available space)
:>		Right aligns the result (within the available space)
:^		Center aligns the result (within the available space)
:=		Places the sign to the left most position
:+		Use a plus sign to indicate if the result is positive or negative
:-		Use a minus sign for negative values only
: 		Use a space to insert an extra space before positive numbers (and a minus sign before negative numbers)
:,		Use a comma as a thousand separator
:_		Use a underscore as a thousand separator
:b		Binary format
:c		Converts the value into the corresponding Unicode character
:d		Decimal format
:e		Scientific format, with a lower case e
:E		Scientific format, with an upper case E
:f		Fix point number format
:F		Fix point number format, in uppercase format (show inf and nan as INF and NAN)
:g		General format
:G		General format (using a upper case E for scientific notations)
:o		Octal format
:x		Hex format, lower case
:X		Hex format, upper case
:n		Number format
:%		Percentage format
'''

# For example, we force the number displayed to have a sign in front, even if positive.
price = 1000
txt = f"The price is {price:+} dollars"
print(txt)

# What if binary? 
price = 1024
txt = f"The price is {price:b} dollars"
print(txt)

# Underscore as a thousand separator.
price = 551234*865
txt = f"The price is {price:_} dollars"
print(txt)

# Fix point number format.
price = 554.36211*865.2817
txt = f"The price is {price:f} dollars"
print(txt)

# ======================================================================= <<<<<





