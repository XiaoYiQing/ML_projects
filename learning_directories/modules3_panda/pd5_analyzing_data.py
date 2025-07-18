



# ======================================================================= >>>>>
#	DataFrames Analysis
# ======================================================================= >>>>>

import os
import pandas as pd

# Define the full file name of the target data file.
dirname = os.path.dirname(__file__)
dataFile_baseName = "pd4_data"
dataFile_fullName = f"{dirname}\\test_data\\{dataFile_baseName}.csv"

'''
Viewing the Data
One of the most used method for getting a quick overview of the DataFrame, 
is the head() method.

The head() method returns the headers and a specified number of rows, starting 
from the top.
'''

df = pd.read_csv( dataFile_fullName )

print(df.head(6))
# Note: if the number of rows is not specified, the head() method will return 
# the top 5 rows.


'''
There is also a tail() method for viewing the last rows of the DataFrame.

The tail() method returns the headers and a specified number of rows, 
starting from the bottom.
'''

print(df.tail(4)) 
# Note: if the number of rows is not specified, the tail() method will return 
# the last 5 rows.


print()
'''
Info About the Data
The DataFrames object has a method called info(), that gives you more 
information about the data set.
'''
print(df.info()) 

'''
Null Values
The info() method also tells us how many Non-Null values there are present 
in each column, and in our data set it seems like there are 164 of 169 
Non-Null values in the "Calories" column.

Which means that there are 5 rows with no value at all, in the "Calories" 
column, for whatever reason.

Empty values, or Null values, can be bad when analyzing data, and you should 
consider removing rows with empty values. This is a step towards what is 
called cleaning data, and you will learn more about that in the next chapters.
'''

# ======================================================================= <<<<<

