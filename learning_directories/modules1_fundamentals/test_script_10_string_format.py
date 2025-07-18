
'''
Recall that standard combination of string and number variables is not allowed.
For example:
	a = 'My string'
	b = 36
	a + b [ <- error ]
	
The format() function solves this issue.
'''
	
	
# The format() method takes the passed arguments, formats them, and places them in the string where the placeholders {} are:
age = 36
txt = "My name is John, and I am {}"
print(txt.format(age))


# The format() method takes unlimited number of arguments, and are placed into the respective placeholders:
quantity = 3
itemno = 567
price = 49.95
myorder = "I want to pay {} dollars for {} pieces of item {}."
print(myorder.format(quantity, itemno, price))


# You can use index numbers {0} to be sure the arguments are placed in the correct placeholders:
quantity = 3
itemno = 567
price = 49.95
myorder = "I want to pay {2} dollars for {0} pieces of item {1}."
print(myorder.format(quantity, itemno, price))

