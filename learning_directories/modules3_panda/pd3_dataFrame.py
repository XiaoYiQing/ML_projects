


'''
What is a DataFrame?
A Pandas DataFrame is a 2 dimensional data structure, like a 2 
dimensional array, or a table with rows and columns.
'''


# ======================================================================= >>>>>
#	DataFrame
# ======================================================================= >>>>>

import pandas as pd

data = {
  "calories": [420, 380, 390],
  "duration": [50, 40, 45]
}

#load data into a DataFrame object:
df = pd.DataFrame(data)

print( "The dataFrame:" )
print( '\t' + str( df ).replace('\n', '\n\t' ) ) 


# Locate Row:
# As you can see from the result above, the DataFrame is like a table with 
# rows and columns.
# Pandas use the loc attribute to return one or more specified row(s)

# refer to the row index:
print( "Row 0 is:" )
print( '\t' + str( df.loc[0] ).replace('\n', '\n\t' ) )
print( "Note: notice the returned value is a (Pandas) series" )
# Note: This example returns a Pandas Series.

print()

# Return multiple rows:
print( "Row 0 and 1 are:" )
print( '\t' + str( df.loc[[0,1]] ).replace('\n', '\n\t' ) ) 
print( "Note: When using [], the returned value is a (Pandas) DataFrame." )

# ======================================================================= <<<<<

print()

# ======================================================================= >>>>>
#	DataFrame: Named Indexes
# ======================================================================= >>>>>

'''
With the index argument, you can name your own indexes.
'''

df = pd.DataFrame(data, index = ["day1", "day2", "day3"])
print( "The dataFrame with named indexes:" )
print( '\t' + str( df ).replace('\n', '\n\t' ) )

#refer to the named index:
print( "Row 'day2' is:" )
print( '\t' + str( df.loc[2221308] ).replace('\n', '\n\t' ) )

# ======================================================================= <<<<<



