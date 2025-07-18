


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
#	Data Cleaning: Replace Using Mean, Median, or Mode
# ======================================================================= >>>>>

'''
A common way to replace empty cells, is to calculate the mean, median or 
mode value of the column.

Pandas uses the mean() median() and mode() methods to calculate the respective 
values for a specified column:
'''

# Mean = the average value (the sum of all values divided by number of values).
# Calculate the MEAN, and replace any empty values with it:
x_mean = df["Calories"].mean()
print(f"The mean of the column 'Calories': {x_mean}")
#
new_df = df.fillna( {"Calories":x_mean} )
print("The rows with empty cells (replaced with mean at 'Calories' column) now look like:")
print(new_df.loc[[6,8,12]])


print()
# Median = the value in the middle, after you have sorted all values ascending.
# Calculate the MEDIAN, and replace any empty values with it:
x_median = df["Calories"].median()
print(f"The median of the column 'Calories': {x_median}")
#
new_df = df.fillna( {"Calories":x_median} )
print("The rows with empty cells (replaced with median at 'Calories' column) now look like:")
print(new_df.loc[[6,8,12]])


print()
# Mode = the value that appears most frequently.
x_mode = df["Calories"].mode()[0]
print(f"The mode of the column 'Calories': {x_mode}")
#
new_df = df.fillna( {"Calories":x_mode} )
print("The rows with empty cells (replaced with mode at 'Calories' column) now look like:")
print(new_df.loc[[6,8,12]])

# ======================================================================= <<<<<






