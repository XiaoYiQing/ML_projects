


'''
What is a Series?
A Pandas Series is like a column in a table.

It is a one-dimensional array holding data of any type.
'''


# ======================================================================= >>>>>
#	Series
# ======================================================================= >>>>>

import pandas as pd

a = [1, 7, 2]

myvar = pd.Series(a)

print(f"Printing the series with labelling (1st col = indices, 2nd col = data):")
print( '\t' + str( myvar ).replace('\n', '\n\t' ) )

'''
Labels
If nothing else is specified, the values are labeled with their index number. 
First value has index 0, second value has index 1 etc.

This label can be used to access a specified value.
'''

print( f"Unlabeled series access specific values using indices" )
print( f"\tFor example, myvar[0]: {myvar[0]}" )


# With the index argument, you can name your own labels.
myvar = pd.Series( a, index = ["x", "y", "z"] )
print(f"Printing the series with labelling (1st col = labels, 2nd col = data):")
print( '\t' + str( myvar ).replace('\n', '\n\t' ) )

# When you have created labels, you can access an item by referring to the label.
print( f"Can access data using label reference: \n\tmyvar['y'] = {myvar['y']}" )

# ======================================================================= <<<<<

print()

# ======================================================================= >>>>>
#	Series: Key/Value Objects
# ======================================================================= >>>>>

'''
You can also use a key/value object, like a dictionary, when creating a Series.
'''

calories = {"day1": 420, "day2": 380, "day3": 390}
print( f"A dictionary: {calories}" )

# Note: The keys of the dictionary become the labels.
myvar = pd.Series(calories)
print(f"Printing the series generated using the dictionary:")
print( '\t' + str( myvar ).replace('\n', '\n\t' ) )


# To select only some of the items in the dictionary, use the index argument 
# and specify only the items you want to include in the Series.
myvar = pd.Series(calories, index = ["day1", "day2"])
print( "Printing the series generated using the library with index specified \
for only 'day1' and 'day2':")
print( '\t' + str( myvar ).replace('\n', '\n\t' ) )

# ======================================================================= <<<<<
