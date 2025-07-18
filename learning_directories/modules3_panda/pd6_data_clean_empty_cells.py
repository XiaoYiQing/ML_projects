


'''
Data Cleaning
Data cleaning means fixing bad data in your data set.

Bad data could be:

Empty cells
Data in wrong format
Wrong data
Duplicates
In this tutorial you will learn how to deal with all of them.
'''

# ======================================================================= >>>>>
#	Data Cleaning: Initialization
# ======================================================================= >>>>>

import os
import pandas as pd

# Define the full file name of the target data file.
dirname = os.path.dirname(__file__)
dataFile_baseName = "pd6_data_red"
dataFile_fullName = f"{dirname}\\test_data\\{dataFile_baseName}.csv"

df = pd.read_csv( dataFile_fullName )

'''
The data set contains:
> some empty cells (rows 8, 10, and 14).
> wrong format (row 12).
> wrong data (row 3).
> duplicates (rows 5 and 6).
'''

# ======================================================================= <<<<<


# ======================================================================= >>>>>
#	Data Cleaning: Eliminate Empty Cell Rows
# ======================================================================= >>>>>

'''
Remove Rows
One way to deal with empty cells is to remove rows that contain empty cells.

This is usually OK, since data sets can be very big, and removing a few rows 
will not have a big impact on the result.
'''

# Eliminate rows containing empty cells.
new_df = df.dropna()
# Note: By default, the dropna() method returns a new DataFrame, and will 
# not change the original. You can force the original dataFrame to receive
# the change if you use the "inplace = True" argument:
#   df.dropna(inplace = True)
# Note: Now, the dropna(inplace = True) will NOT return a new DataFrame, but 
# it will remove all rows containing NULL values from the original DataFrame.

print( new_df.info() )
# Looking at the infomartion list of the modified dataFrame, we notice that we 
# now only have 11 rows rather than 14 rows in the original.

# ======================================================================= <<<<<

print()

# ======================================================================= >>>>>
#	Data Cleaning: Replace Empty Cells
# ======================================================================= >>>>>
'''
Replace Empty Values
Another way of dealing with empty cells is to insert a new value instead.

This way you do not have to delete entire rows just because of some empty cells.

The fillna() method allows us to replace empty cells with a value:
'''

# Replace NULL values with the number 130:
new_df = df.fillna( 130 )
print("The rows with empty cells (replaced with 130) now look like:")
print(new_df.loc[[6,8,12]])

# Note: By default, the fillna() method returns a new DataFrame, and will 
# not change the original. You can force the original dataFrame to receive
# the change if you use the "inplace = True" argument:
# ======================================================================= <<<<<

print()

# ======================================================================= >>>>>
#	Data Cleaning: Replace Empty Cells at Specified Columns
# ======================================================================= >>>>>

'''
The example above replaces all empty cells in the whole Data Frame.

To only replace empty values for one column, specify the column name for 
the DataFrame:
'''

# Replace NULL values with the number 130 specifically within column "Calories":
new_df = df.copy(deep=True)
new_df.fillna( {"Calories":130}, inplace = True )
print("The rows with empty cells (replaced with 130 at 'Calories' column) now look like:")
print(new_df.loc[[6,8,12]])
# ======================================================================= <<<<<



