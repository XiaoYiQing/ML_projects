
# String variables have access to built-in class methods.


# Turn all letters to upper case.
a = "Hello, World 123!"
print(a.upper())

# Turn all letters to upper case.
a = "Hello, World 123!"
print(a.lower())

# Remove white space at beginning and end of the string.
a = "   Hello, World!   "
print(a.strip()) # returns "Hello, World!"

# Replace a string with another string.
a = "Hello, Horld!"
print(a.replace("H", "J"))
a = "Hello, Hell!"
print(a.replace("He", "Sa"))

# Splits the string into substrings if it finds instances of the separator:
a = "Hello, one, two, three!"
print(a.split(",")) # returns ['Hello', ' World!']


# Merge variable a with variable b into variable c:
a = "Hello"
b = "World"
c = a + b
print(c)
