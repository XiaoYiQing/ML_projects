



# ======================================================================= >>>>>
#	For Loops
# ======================================================================= >>>>>

# The else keyword in a for loop specifies a block of code to be executed when the loop is finished:
for x in range(6):
  print( x, end = ' ' )
else:
  print("\nFinally finished!")
# The else block will NOT be executed if the loop is stopped by a break statement.


# Break the loop when x is 3, and see what happens with the else block:
for x in range(6):
  if x == 3: break
  print(x)
else:
  print("Finally finished!")

# A nested loop is a loop inside a loop.
# The "inner loop" will be executed one time for each iteration of the "outer loop":
adj = ["red", "big", "tasty"]
fruits = ["apple", "banana", "cherry"]
for x in adj:
  for y in fruits:
    print( x, y, end = ' ' )
  print()


# for loops cannot be empty, but if you for some reason have a for loop with no content, put in the pass statement to avoid getting an error.
for x in [0, 1, 2]:
  pass



# ======================================================================= <<<<<


