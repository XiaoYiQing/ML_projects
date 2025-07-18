


'''
Data of Wrong Format
Cells with data of wrong format can make it difficult, or even impossible, 
to analyze data.

To fix it, you have two options: remove the rows, or convert all cells in 
the columns into the same format.
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
#	Data Cleaning: Wrong Data Format
# ======================================================================= >>>>>

# Let's try to convert all cells in the 'Date' column into dates.
# Pandas has a to_datetime() method for this:
df['Date'] = pd.to_datetime( df['Date'], yearfirst = True, format='mixed' )
print( df['Date'] )

# Removing Rows
# The result from the converting in the example above gave us a NaT value, 
# which can be handled as a NULL value, and we can remove the row by using 
# the dropna() method.
df.dropna(subset=['Date'], inplace = True)
print( df['Date'] )

'''
Notice that the indexing now is missing index 8 (Indexing is not updated 
after row removal). 
This is to account for when labeling is not indexing. For example, if my labels
were 'apple', 'orange', 'banana', etc. rather than 0, 1, 2, etc., you cannot
'update' the labeling when a row is deleted.

However, if you want  sequential indexing, you can reset your indexing using 
the following command:
    df.reset_index()
'''



# ======================================================================= <<<<<
