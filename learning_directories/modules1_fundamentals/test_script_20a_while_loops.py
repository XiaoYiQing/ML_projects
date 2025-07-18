


# ======================================================================= >>>>>
#	While Loops
# ======================================================================= >>>>>

# With the while loop we can execute a set of statements as long as a condition is true.
i = 1
while i < 6:
  print( i, end = ' ' )
  i += 1
print()


# With the break statement we can stop the loop even if the while condition is true:
i = 1
while i < 6:
  print( i, end = ' ' )
  if i == 3:
    break
  i += 1
print()

# With the continue statement we can stop the current iteration, and continue with the next:
i = 0
while i < 6:
  i += 1
  if i == 3:
    continue
  print( i, end = ' ' )
print()
  

# With the else statement we can run a block of code once when the condition no longer is true:
i = 1
while i < 7:
  print( i, end = ' ' )
  i += 1
else:
  print("\ni is no longer less than 6")
  
# ======================================================================= <<<<<


