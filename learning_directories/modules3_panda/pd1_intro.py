


'''
Pandas is a Python library used for working with data sets.

It has functions for analyzing, cleaning, exploring, and manipulating 
data.

The name "Pandas" has a reference to both "Panel Data", and "Python 
Data Analysis" and was created by Wes McKinney in 2008.
'''

'''
Why Use Pandas?
Pandas allows us to analyze big data and make conclusions based on 
statistical theories.

Pandas can clean messy data sets, and make them readable and relevant.

Relevant data is very important in data science.
'''

'''
What Can Pandas Do?
Pandas gives you answers about the data. Like:
    Is there a correlation between two or more columns?
    What is average value?
    Max value?
    Min value?
Pandas are also able to delete rows that are not relevant, or contains 
wrong values, like empty or NULL values. This is called cleaning the data.
'''

'''
Where is the Pandas Codebase?
The source code for Pandas is located at this github repository 
https://github.com/pandas-dev/pandas
'''

# ======================================================================= >>>>>
#	Pandas: Basic Use
# ======================================================================= >>>>>

import pandas as pd
print(f"Pandas version: {pd.__version__}")

mydataset = {
  'cars': ["BMW", "Volvo", "Ford"],
  'passings': [3, 7, 2]
}

myvar = pd.DataFrame(mydataset)
print("Data frame: ")
print(myvar)

# ======================================================================= <<<<<


