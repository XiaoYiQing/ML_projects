



# ======================================================================= >>>>>
#	Python String Formatting
# ======================================================================= >>>>>

'''
F-String was introduced in Python 3.6, and is now the preferred way of formatting strings.

Before Python 3.6 we had to use the format() method.
'''


# F-string allows you to format selected parts of a string.
# To specify a string as an f-string, simply put an f in front of the string literal, like this:
txt = f"The price is 49 dollars"
print(txt)

# To format values in an f-string, add placeholders {}.
# A placeholder can contain variables, operations, functions, and modifiers to format the value.
price = 59
txt = f"The price is {price} dollars"
print(txt)


# A placeholder can also include a modifier to format the value.
# A modifier is included by adding a colon : followed by a legal formatting type, like .2f which means fixed point number with 2 decimals:
price = 59
txt = f"The price is {price:.2f} dollars"
print(txt)

# You can also format a value directly without keeping it in a variable:
txt = f"The price is {95:.2f} dollars"
print(txt)

# ======================================================================= <<<<<


# ======================================================================= >>>>>
#	String Formatting: Perform Operations in F-Strings
# ======================================================================= >>>>>

# You can perform Python operations inside the placeholders.
# You can do math operations:
txt = f"The price is {20 * 59} dollars"
print(txt)

# You can perform math operations on variables:
price = 59
tax = 0.25
txt = f"The price is {price + (price * tax)} dollars"
print(txt)

# You can perform if...else statements inside the placeholders:
price = 49
txt = f"It is very {'Expensive' if price>50 else 'Cheap'}"
print(txt)

# ======================================================================= <<<<<





