



'''
When your data has different values, and even different measurement units, 
it can be difficult to compare them. What is kilograms compared to meters? 
Or altitude compared to time?

The answer to this problem is scaling. 
We can scale data into new values that are easier to compare.


There are different methods for scaling data, in this tutorial we will use a method called 
standardization.
The standardization method uses this formula:
	z = (x - u) / s
Where 
	z is the new value
	x is the original value
	u is the mean
	s is the standard deviation
'''


# ======================================================================= >>>>>
#	Scale Features
# ======================================================================= >>>>>

import os
import pandas
from sklearn import linear_model
from sklearn.preprocessing import StandardScaler


# The Python sklearn module has a method called StandardScaler() which returns a 
# Scaler object with methods for transforming data sets.
scale = StandardScaler()


# Define the full file name of the target data file.
dirname = os.path.dirname(__file__)
dataFile_baseName = "ML_09_test_data";
dataFile_fullName = f"{dirname}\\test_data\\{dataFile_baseName}.csv"

# The Pandas module allows us to read csv files and return a DataFrame object.
df = pandas.read_csv( dataFile_fullName )

X = df[['Weight', 'Volume']]
origX = X.values
scaledX = scale.fit_transform(origX)

for i in range(4):
	str_var = f"Weight and volume at index {i} bef. scaling: {origX[i]}"
	print( str_var )
	str_var = f"Weight and volume at index {i} aft. scaling: {scaledX[i]}"
	print( str_var )
	
print( "etc." )


# The task in the Multiple Regression chapter was to predict the CO2 
# emission from a car when you only knew its weight and volume.

# When the data set is scaled, you will have to use the scale when you predict values:
y = df['CO2']

# Create a linear regression object.
regr = linear_model.LinearRegression()
# Takes the scaled independent and dependent values as parameters and fills the regression 
# 	object with data that describes the relationship
regr.fit(scaledX, y.values)


# Define target independent variables to predict upon:
prediction = [ [2300, 1300], [2000, 1100] ]
# Scale the indep. variables.
scaled_predict = scale.transform( prediction )

# Obtain the CO2 predictions.
predictedCO2 = regr.predict(scaled_predict)
print( predictedCO2 )

# ======================================================================= <<<<<


