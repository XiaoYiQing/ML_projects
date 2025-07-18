


# ======================================================================= >>>>>
#	Logical Operator
# ======================================================================= >>>>>

a = 200
b = 33
c = 500

# The and keyword is a logical operator, and is used to combine conditional statements:
if a > b and c > a:
  print("Both conditions are True")
  
# Test if a is greater than b, OR if a is greater than c:
if a > b or a > c:
  print("At least one of the conditions is True")

# Test if a is NOT greater than b:
if not a > b:
  print("a is NOT greater than b")

# ======================================================================= <<<<<


# ======================================================================= >>>>>
#	The pass Statement
# ======================================================================= >>>>>
# if statements cannot be empty, but if you for some reason have an if statement with no content, put in the pass statement to avoid getting an error.
a = 33
b = 200

if b > a:
  pass
# ======================================================================= <<<<<






