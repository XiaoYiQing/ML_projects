


'''
Read CSV Files
A simple way to store big data sets is to use CSV files (comma separated files).

CSV files contains plain text and is a well know format that can be read by 
everyone including Pandas.

In our examples we will be using a CSV file called 'data.csv'.
'''

# ======================================================================= >>>>>
#	csv: Read
# ======================================================================= >>>>>

import os
import pandas as pd

# Define the full file name of the target data file.
dirname = os.path.dirname(__file__)
dataFile_baseName = "pd4_data"
dataFile_fullName = f"{dirname}\\test_data\\{dataFile_baseName}.csv"

df = pd.read_csv( dataFile_fullName )

# Print a portion of the data frame.
prt_cnt = 3
tar_range_1 = range(prt_cnt)
print(df.loc[tar_range_1]) 
print("...")
idx_cnt = len(df.index)
tmp = range(idx_cnt-prt_cnt,idx_cnt,1)
tar_range_2 = df.index[tmp]
print(df.loc[tar_range_2]) 

print()
# If you have a large DataFrame with many rows, Pandas will only return 
# the first 5 rows, and the last 5 rows:
print(df)

# Tip: use to_string() to print the entire DataFrame.
# print(df.to_string()) 

print()
'''
max_rows
The number of rows returned is defined in Pandas option settings.

You can check your system's maximum rows with the pd.options.display.max_rows 
statement.
'''

print(f"The result of command: 'pd.options.display.max_rows': \n\t{pd.options.display.max_rows}")
print( "60 is the default maximum number of rows that will be printed.\
 A dataFrame having beyond 60 rows will only have the first and last 5 rows be printed." )

# You can change the maximum rows number with the same statement.
# pd.options.display.max_rows = 9999
# df = pd.read_csv('data.csv')
# print(df) 

# ======================================================================= <<<<<


