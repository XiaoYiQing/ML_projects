


'''
Duplicate rows are rows that have been registered more than one time.

To discover duplicates, we can use the duplicated() method.

The duplicated() method returns a Boolean values for each row.
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
#	Data Cleaning: Duplicates
# ======================================================================= >>>>>

# Returns True for every row that is a duplicate, otherwise False:
print( df.duplicated() )
# Note: 1st instance of the duplicated row is not considered a duplicate.

# Removing Duplicates
# To remove duplicates, use the drop_duplicates() method.
idx_arr = range(6)
print( "Before dropping duplicates:" )
print( df.loc[idx_arr] )
df.drop_duplicates( inplace = True )
# Although the duplicated rows are now deleted, the sequential indexing is not 
# updated. Thus, we use the reset_index() function to update the modified dataFrame.
# Note: the 'drop=True' command is needed so as to avoid creating a column that
# saves the previous indexing column in the dataFrame.
df.reset_index( inplace = True, drop = True )
print( "After dropping duplicates:" )
print( df.loc[idx_arr] )

# ======================================================================= <<<<<


