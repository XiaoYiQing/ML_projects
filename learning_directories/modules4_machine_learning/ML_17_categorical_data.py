


'''
When your data has categories represented by strings, it will be 
difficult to use them to train machine learning models which often 
only accepts numeric data.

Instead of ignoring the categorical data and excluding the information 
from our model, you can tranform the data so it can be used in your models.

Take a look at the table below, it is the same data set that we used in 
the multiple regression chapter.
'''


# ======================================================================= >>>>>
#	Categorical Data
# ======================================================================= >>>>>

import os
import pandas as pd
from sklearn import linear_model


dirname = os.path.dirname(__file__)
dataFile_baseName = "ML_09_test_data"
dataFile_fullName = f"{dirname}\\test_data\\{dataFile_baseName}.csv"

cars = pd.read_csv( dataFile_fullName )
# print( cars.to_string() )

# In the multiple regression chapter, we tried to predict the CO2 emitted 
# based on the volume of the engine and the weight of the car but we excluded 
# information about the car brand and model.
# The information about the car brand or the car model might help us make a 
# better prediction of the CO2 emitted.

# ======================================================================= <<<<<


# ======================================================================= >>>>>
#	Categorical Data (One Hot Encoding)
# ======================================================================= >>>>>

# We must have a numeric representation of the categorical variable. 
# One way to do this is to have a column representing each group in the category.
# For each column, the values will be 1 or 0 where 1 represents the inclusion of 
# the group and 0 represents the exclusion. This transformation is called one 
# hot encoding.

# You do not have to do this manually, the Python Pandas module has a function 
# that called get_dummies() which does one hot encoding.

ohe_cars = pd.get_dummies(cars[['Car']])
# print(ohe_cars.to_string())
# A column was created for every car brand in the Car column.

'''
We can use this additional information alongside the volume and weight to 
predict CO2
To combine the information, we can use the concat() function from pandas.
'''

X = pd.concat( [ cars[['Volume', 'Weight']], ohe_cars ], axis=1 )
y = cars['CO2']

# Now we can fit the data to a linear regression:
regr = linear_model.LinearRegression()
regr.fit(X.values,y.values)
# We now have a coefficient for the volume, the weight, and each car 
# brand in the data set


# predict the CO2 emission of a Volvo where the weight is 2300kg, and 
# the volume is 1300cm3:
predictedCO2 = regr.predict([[2300, 1300,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0]])

str_var = f"The CO2 emission of a Volve with 2300kg and 1300cm^3: {predictedCO2}"
print(str_var)

# ======================================================================= <<<<<



# ======================================================================= >>>>>
#	Dummifying
# ======================================================================= >>>>>

'''
It is not necessary to create one column for each group in your 
category. The information can be retained using 1 column less than 
the number of groups you have.

For example, you have a column representing colors and in that column, 
you have three colors: red, blue, and green.
'''

colors = pd.DataFrame({'color': ['blue', 'red', 'green']})
print(colors)

'''
You can create 2 columns holding permutation of logic map of:
    is red 
    is green
    neither 

To do this, we can use the function get_dummies and then drop 
one of the columns. 
There is an argument, drop_first, which allows us to exclude the 
first column from the resulting table.
'''

dummies = pd.get_dummies(colors, drop_first=True)
dummies['color'] = colors['color']
print(dummies)

# All three colors can be uniquely determined through 2 boolean values.

# ======================================================================= <<<<<


