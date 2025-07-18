


'''
Finding Relationships
A great aspect of the Pandas module is the corr() method.

The corr() method calculates the relationship between each column in your 
data set.

Note: The corr() method ignores "non-numeric" columns.
'''


# ======================================================================= >>>>>
#	Initialization
# ======================================================================= >>>>>

import os
import pandas as pd

# Define the full file name of the target data file.
dirname = os.path.dirname(__file__)
dataFile_baseName = "pd10_data"
dataFile_fullName = f"{dirname}\\test_data\\{dataFile_baseName}.csv"

df = pd.read_csv( dataFile_fullName )

# ======================================================================= <<<<<


# ======================================================================= >>>>>
#	Data Correlation
# ======================================================================= >>>>>

# Show the relationship between the columns:
corr_res = df.corr()
print( "Correlation function results:" )
print( corr_res )

'''
Result Explained
The Result of the corr() method is a table with a lot of numbers that represents 
how well the relationship is between two columns.

The number varies from -1 to 1.

1 means that there is a 1 to 1 relationship (a perfect correlation), and for 
this data set, each time a value went up in the first column, the other one 
went up as well.

0.9 is also a good relationship, and if you increase one value, the other will 
probably increase as well.

-0.9 would be just as good relationship as 0.9, but if you increase one value, 
the other will probably go down.

0.2 means NOT a good relationship, meaning that if one value goes up does not 
mean that the other will.
'''

# ======================================================================= <<<<<
