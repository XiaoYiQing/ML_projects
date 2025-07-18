
'''
There are 4 main types of collection data in python:
	List is a collection with the following traits: 
		ordered 
		changeable
		indexed
		can duplicate members.
	Tuple is a collection with the following traits: 
		ordered 
		unchangeable
		indexed
		can duplicate members.
	Set is a collection with the following traits:
		unordered
		unchangeable* (But you can add and remove items), 
		unindexed
		no duplicate members.
	Dictionary is a collection with the following traits:
		ordered** 
		changeable
		indexed
		no duplicate members.
'''


# ===== Lists can contain data of different types:
list1 = ["abc", 34, True, 40, "male"]
print( list1 )
# List is its own data type.
print( type( list1 ) )
print()

# ===== Negative Indexing =====
# -1 refers to the last item, -2 refers to the second last item etc.
thislist = ["apple", "banana", "cherry"]
print(thislist[-1])
print()

# ===== Range of Indexes =====
# The search will start at index 2 (included) and end at index 5 (not included).
thislist = ["apple", "banana", "cherry", "orange", "kiwi", "melon", "mango"]
print(thislist[2:5])
# By leaving out the start value, the range will start at the first item:
print(thislist[:4])
# By leaving out the end value, the range will go on to the end of the list:
print(thislist[3:])
# This example returns the items from "orange" (-4) to, but NOT including "mango" (-1):
print(thislist[-4:-1])
# This example returns the items from "orange" (-4) to "mango" (-1):
print(thislist[-4:])
print()


# ===== Loop Through a List =====
thislist = ["apple", "banana", "cherry"]
for x in thislist:
  print(x)
# You can also loop through the list items by referring to their index number.
for i in range(len(thislist)):
  print(thislist[i])
# Print all items, using a while loop to go through all the index numbers
i = 0
while i < len(thislist):
  print(thislist[i])
  i = i + 1

# List Comprehension offers the shortest syntax for looping through lists.
# A short hand for loop that will print all items in a list:
[print(x) for x in thislist]

print()




