


'''

Regression:
The term regression is used when you try to find the relationship between variables.
In Machine Learning, and in statistical modeling, that relationship is used to predict the outcome of future events.


Linear Regression:
Linear regression uses the relationship between the data-points to draw a straight line through all them.
This line can be used to predict future values.

Python has methods for finding a relationship between data-points and to draw a line of linear regression.

'''

# ======================================================================= >>>>>
#	Linear Regression
# ======================================================================= >>>>>

import matplotlib.pyplot as plt
from scipy import stats


# In the example below, the x-axis represents age, and the y-axis represents speed. 
# We have registered the age and speed of 13 cars as they were passing a tollbooth. 
# Let us see if the data we collected could be used in a linear regression:



x = [5,7,8,7,2,17,2,9,4,11,12,9,6]
y = [99,86,87,88,111,86,103,87,94,78,77,85,86]

# plt.scatter(x, y)
# plt.show()


# Perform linear regression:
linRegrRes = stats.linregress(x, y)
slope = linRegrRes.slope
intercept = linRegrRes.intercept
rValue = linRegrRes.rvalue
pValue = linRegrRes.pvalue
stdErr = linRegrRes.stderr

# Define temporary function for the linear function produced by the linear regression.
def myfunc(x):
  return slope * x + intercept

# Run each value of the x array through the function. 
# This will result in a new array with new values for the y-axis:
mymodel = list(map(myfunc, x))


plt.scatter(x, y)
plt.plot(x, mymodel)
plt.show()


# The r value ranges from -1 to 1, where 0 means no relationship, and 1 (and -1) means 100% related.
str_var = f"r value = {rValue}"
print( str_var )
# The result -0.76 shows that there is a relationship, not perfect, but it indicates that we could use linear regression in future predictions.

# You should discard the linear regression result if this value is too close to 0 (Bad fit).

# ======================================================================= <<<<<









