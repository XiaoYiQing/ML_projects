



'''

In Machine Learning we create models to predict the outcome of certain events, 
like in the previous chapter where we predicted the CO2 emission of a car when 
we knew the weight and engine size.

To measure if the model is good enough, we can use a method called Train/Test.

Train/Test is a method to measure the accuracy of your model.

It is called Train/Test because you split the data set into two sets: 
	a training set 
	a testing set.

'''

import numpy
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score
numpy.random.seed(2)


# ======================================================================= >>>>>
#	Training and Testing
# ======================================================================= >>>>>
init_set_cnt = 100
# Define number of minutes before making a purchase.
x = numpy.random.normal(3, 1, init_set_cnt)
# Define amount of money spent on the purchase.
y = numpy.random.normal(150, 40, init_set_cnt)
y = y / x

# plt.scatter(x, y)
# plt.show()

sep_idx = 80
# The training set should be a random selection of of the original data.
train_x = x[:sep_idx]
train_y = y[:sep_idx]
# The testing set should be the remaining data.
test_x = x[sep_idx:]
test_y = y[sep_idx:]

# ======================================================================= <<<<<


# ======================================================================= >>>>>
#	Testing Set Verify
# ======================================================================= >>>>>

# It is necessary to verify if the training and testing sets are good enough 
# representation of the original set.

# plt.scatter(train_x, train_y)
# plt.show()
# plt.scatter(test_x, test_y)
# plt.show()

# We avoid running the graphs here, but you get the idea: 
#	Look if the scatter plots are similar to the original scatter plot.

# ======================================================================= <<<<<


# ======================================================================= >>>>>
#	Fit the Data Set
# ======================================================================= >>>>>

# Use polynomial regression to fit the training set.
mymodel = numpy.poly1d( numpy.polyfit( train_x, train_y, 4 ) )

# Define a sample array covering the expected X-axis range.
x_samp = numpy.linspace(0, 6, 100)
# Compute the sample array of corresponding Y-axis values.
y_samp = mymodel(x_samp)

# Plot the results, with the approximation function line drawn over the scatter range.
# plt.scatter( train_x, train_y )
# plt.plot( x_samp, y_samp )
# plt.show()

# ======================================================================= <<<<<


# ======================================================================= >>>>>
#	R-squared
# ======================================================================= >>>>>

'''

In statistics, the coefficient of determination, denoted R^2 or r^2 and pronounced 
"R squared", is the proportion of the variation in the dependent variable that is 
predictable from the independent variable(s).

It measures the relationship between the x axis and the y axis, 
and the value ranges from 0 to 1, where 0 means no relationship, 
and 1 means totally related.

'''

# Assess the R^2 score of the training data set.
r2_train = r2_score( train_y, mymodel( train_x ) )
str_var = f"The R^2 score of the trained data set: {r2_train}"
print( str_var )

# R^2 = ~0.8 is an ok score. So the model is a sensible model.


# Assess the R^2 score the test data set.
r2_test = r2_score( test_y, mymodel( test_x ) )
str_var = f"The R^2 score of the trained data set: {r2_test}"
print( str_var )

# ======================================================================= <<<<<



# Now that we have established that our model is OK, 
# we can start predicting new values.
predict_x = 5
str_var = f"The model prediction for amount a customer dishes out after waiting {predict_x} min(s): {mymodel(predict_x)}"
print( str_var )




