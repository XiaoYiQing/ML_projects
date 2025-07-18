

# Defining the string over several lines this way ensure it is printed while maitaining the same line break pattern.
a = """Lorem ipsum dolor sit amet,
consectetur adipiscing elit,
sed do eiusmod tempor incididunt
ut labore et dolore magna aliqua.\n"""

print(a)



# Like many other popular programming languages, strings in Python are arrays of bytes representing unicode characters.
# However, Python does not have a character data type, a single character is simply a string with a length of 1.
# Square brackets can be used to access elements of the string.

a = "Hello, World!"
print(a[1])

# You can parse through a string array using for loop.
for x in "abc":
  print(x)

# You can obtain the number of characters in a string.
a = "Hello, World!"
b = len(a)
print(b)


# You can check if a certain phrase or character is present in a string using the keyword 'in'.
txt = "The best things in life are free!"
b = "free" in txt
print(b)

# You can check if a certain phrase or character is NOT present in a string using the keyword 'not in'.
txt = "The best things in life are free!"
b = "free" not in txt
print(b)



