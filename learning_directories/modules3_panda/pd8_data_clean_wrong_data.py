


'''
Wrong Data

"Wrong data" does not have to be "empty cells" or "wrong format", it can 
just be wrong, like if someone registered "199" instead of "1.99".

Sometimes you can spot wrong data by looking at the data set, because you 
have an expectation of what it should be.

If you take a look at our data set, you can see that in row 3, the duration 
is 450, but for all the other rows the duration is between 30 and 60.

It doesn't have to be wrong, but taking in consideration that this is the 
data set of someone's workout sessions, we conclude with the fact that this 
person did not work out in 450 minutes.
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
#	Data Cleaning: Wrong Data
# ======================================================================= >>>>>

'''
Replacing Values
One way to fix wrong values is to replace them with something else.

In our example, it is most likely a typo, and the value should be "45" instead 
of "450", and we could just insert "45" in row 3:
'''

df.loc[1, 'Duration'] = 45
print( df['Duration'] )


'''
For small data sets you might be able to replace the wrong data one by one, 
but not for big data sets.

To replace wrong data for larger data sets you can create some rules, e.g. set 
some boundaries for legal values, and replace any values that are outside of 
the boundaries.
'''

# Loop through all values in the "Duration" column.
# If the value is higher than 120, set it to 120:
for x in df.index:
  if df.loc[ x, "Duration" ] > 120:
    df.loc[ x, "Duration" ] = 120

'''
Another way of handling wrong data is to remove the rows that contains wrong 
data.

This way you do not have to find out what to replace them with, and there is 
a good chance you do not need them to do your analyses.
'''
for x in df.index:
  if df.loc[x, "Duration"] > 120:
    df.drop(x, inplace = True)

# ======================================================================= <<<<<

