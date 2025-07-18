




'''

If your data points clearly will not fit a linear regression (a straight line through all data points), 
it might be ideal for polynomial regression.

Polynomial regression, like linear regression, uses the relationship between the variables x and y 
to find the best way to draw a line through the data points.

'''


# ======================================================================= >>>>>
#	Polynomial Regression
# ======================================================================= >>>>>

import numpy
import matplotlib.pyplot as plt

x = [1,2,3,5,6,7,8,9,10,12,13,14,15,16,18,19,21,22]
y = [100,90,80,60,60,55,60,65,70,70,75,76,78,79,90,99,99,100]

# plt.scatter(x, y)
# plt.show()

# NumPy has a method that lets us make a polynomial model.
# We use 3rd order polynomial to do the job:
mymodel = numpy.poly1d(numpy.polyfit(x, y, 3))

myline = numpy.linspace(x[0], x[:], 100)

plt.scatter(x, y)
plt.plot(myline, mymodel(myline))
plt.show()

# It is important to know how well the relationship between the values of the x- and y-axis is, 
# if there are no relationship the polynomial regression can not be used to predict anything.
# The relationship is measured with a value called the r-squared.
# The r-squared value ranges from 0 to 1, where 0 means no relationship, and 1 means 100% related.

# Python and the Sklearn module will compute this value for you, all you have to do is feed it with the x and y arrays:
from sklearn.metrics import r2_score

r2 = r2_score(y, mymodel(x))
str_var = f"r^2 value = {r2}"
print( str_var )

# You should discard the linear regression result if this value is too close to 0 (Bad fit).


# ======================================================================= <<<<<



