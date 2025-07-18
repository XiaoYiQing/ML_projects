

'''

Multiple regression is like linear regression, but with more than one independent value, 
meaning that we try to predict a value based on two or more variables.

'''

# ======================================================================= >>>>>
#	Multiple Regression
# ======================================================================= >>>>>



import os
import pandas
from sklearn import linear_model

# Define the full file name of the target data file.
dirname = os.path.dirname(__file__)
dataFile_baseName = "ML_09_test_data"
dataFile_fullName = f"{dirname}\\test_data\\{dataFile_baseName}.csv"

# The Pandas module allows us to read csv files and return a DataFrame object.
df = pandas.read_csv( dataFile_fullName )

# Then make a list of the independent values and call this variable X.
# Put the dependent values in a variable called y.
X = df[['Weight', 'Volume']]
y = df['CO2']
# Tip: It is common to name the list of independent values with a upper case X, 
# and the list of dependent values with a lower case y.



# From the sklearn module we will use the LinearRegression() method to 
#	create a linear regression object.
# This object has a method called fit() that takes the independent and dependent 
#	values as parameters and fills the regression object with data that describes the relationship:
regr = linear_model.LinearRegression()
regr.fit(X.values, y.values)

# Predict the CO2 emission of a car where the weight is 2300kg, and the volume is 1300cm3:
tmp = [[2300, 1300],[2000, 1200]]
print(tmp.__class__)
predictedCO2 = regr.predict( tmp )
print(predictedCO2)

# We have predicted that:
#	A car with 1.3 liter engine, and a weight of 2300 kg, will release approximately 107 grams of CO2 for every kilometer it drives.
#	A car with 1.2 liter engine, and a weight of 2000 kg, will release approximately 104 grams of CO2 for every kilometer it drives.

# ======================================================================= <<<<<



# ======================================================================= >>>>>
#	Multiple Regression (Coefficients)
# ======================================================================= >>>>>

'''
The coefficient is a factor that describes the relationship with an unknown variable.

Example: if x is a variable, then 2x is x two times. x is the unknown variable, 
and the number 2 is the coefficient.

In this case, we can ask for the coefficient value of weight against CO2, 
and for volume against CO2. 
The answer(s) we get tells us what would happen if we increase, or decrease, 
one of the independent values.
'''

coeff_list = regr.coef_
Weight_coeff = coeff_list[0]
Volume_coeff = coeff_list[1]

str_var = f"Weight to CO2 coefficient: {Weight_coeff}"
print( str_var )
str_var = f"Volume to CO2 coefficient: {Volume_coeff}"
print( str_var )
# These values tell us that if the weight increase by 1kg, the CO2 emission increases by 0.00755095g.
# And if the engine size (Volume) increases by 1 cm3, the CO2 emission increases by 0.00780526 g.

# ======================================================================= <<<<<




