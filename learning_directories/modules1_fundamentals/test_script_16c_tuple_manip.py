

# ======================================================================= >>>>>
#	Tuple Update
# ======================================================================= >>>>>

# You cannot change a tuple. You have to workaround by converting the tuple into a list first:
x = ("apple", "banana", "cherry")
y = list(x)
y[1] = "kiwi"
x = tuple(y)

# You cannot add to a tuple, so you have to use the same trick.
thistuple = ("apple", "banana", "cherry")
y = list(thistuple)
y.append("orange")
thistuple = tuple(y)

# However, tuples are allowed to be added together:
thistuple = ("apple", "banana", "cherry")
y = ("orange",)
thistuple += y
print(thistuple)

# You cannot remove items from a tuple. Again, you do so using list maneouver again:
thistuple = ("apple", "banana", "cherry")
y = list(thistuple)
y.remove("apple")
thistuple = tuple(y)

# You also have the option of completely delete a tuple:
thistuple = ("apple", "banana", "cherry")
del thistuple
#print(thistuple) #this will raise an error because the tuple no longer exists


# ======================================================================= >>>>>
#	Tuple Unpack
# ======================================================================= >>>>>

# You can unpack a tuple by turning individual items of the tuple to individual variables:
fruits = ("apple", "banana", "cherry")
(green, yellow, red) = fruits
print(green, end=' ')
print(yellow, end=' ')
print(red)


# If the number of variables is less than the number of values, you can add an * to the variable name and the values will be assigned to the variable as a list:
fruits = ("apple", "banana", "cherry", "strawberry", "raspberry")
(green, yellow, *red) = fruits	# Note: 'red' is a list rather than a tuple.
print(green, end=' ')
print(yellow, end=' ')
print(red)

#If the asterisk is added to another variable name than the last, Python will assign values to the variable until the number of values left matches the number of variables left.
fruits = ("apple", "mango", "papaya", "pineapple", "cherry")
(green, *tropic, red) = fruits
print(green)
print(tropic)
print(red)


# ======================================================================= >>>>>
#	Tuple Join
# ======================================================================= >>>>>

# To join two or more tuples you can use the + operator:
tuple1 = ("a", "b" , "c")
tuple2 = (1, 2, 3)
tuple3 = tuple1 + tuple2
print(tuple3)

# If you want to multiply the content of a tuple a given number of times, you can use the * operator:
fruits = ("apple", "banana", "cherry")
mytuple = fruits * 2
print(mytuple)

