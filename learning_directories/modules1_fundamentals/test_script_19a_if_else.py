


# ======================================================================= >>>>>
#	If Else Statements
# ======================================================================= >>>>>

a = 33
b = 200
# Standard if clause definition. The conditional clauses are defined using indentation as opposed to character driven clause delimiation in other languages. For instance, the if clause ends on ealiest instance of a line which begins at the same indent as the 'if' keyword.
if b > a:
  print("b is greater than a")
  
  
# The elif keyword is Python's way of saying "if the previous conditions were not true, then try this condition".
a = 33
b = 33
if b > a:
  print("b is greater than a")
elif a == b:
  print("a and b are equal")
 
# The else keyword catches anything which isn't caught by the preceding conditions.
a = 200
b = 33
if b > a:
  print("b is greater than a")
elif a == b:
  print("a and b are equal")
else:
  print("a is greater than b")


# If you have only one statement to execute, you can put it on the same line as the if statement.
if a > b: print("a is greater than b")
# If you have only one statement to execute, one for if, and one for else, you can put it all on the same line:
print("A") if a > b else print("B")
# You can also have multiple else statements on the same line:
print("A") if a > b else print("=") if a == b else print("B")
# The above are known as Ternary Operators, or Conditional Expressions.

# ======================================================================= <<<<<


# ======================================================================= >>>>>
#	Nested If Else Statements
# ======================================================================= >>>>>
x = 41

# You can have if statements inside if statements, this is called nested if statements.
if x > 10:
  print("Above ten,")
  if x > 20:
    print("and also above 20!")
  else:
    print("but not above 20.")
# ======================================================================= <<<<<










