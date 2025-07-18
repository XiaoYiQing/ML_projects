



'''
Logistic regression aims to solve classification problems. 
It does this by predicting categorical outcomes, unlike 
linear regression that predicts a continuous outcome.

In the simplest case there are two outcomes, which is called binomial, 
an example of which is predicting if a tumor is malignant or benign. 
Other cases have more than two outcomes to classify, in this case it 
is called multinomial. 
A common example for multinomial logistic regression would be predicting 
the class of an iris flower between 3 different species.

Here we will be using basic logistic regression to predict a binomial variable. 
This means it has only two possible outcomes.
'''

import numpy
from sklearn import linear_model

# ======================================================================= >>>>>
#	Logistic Regression
# ======================================================================= >>>>>

# X represents the size of a tumor in centimeters.
X = numpy.array([3.78, 2.44, 2.09, 0.14, 1.72, 1.65, 4.92, 4.37, 4.96, 4.52, 3.69, 5.88])
# Note: X has to be reshaped into a column from a row for the LogisticRegression() 
# function to work.
X = X.reshape(-1,1)

# y represents whether or not the tumor is cancerous (0 for "No", 1 for "Yes").
y = numpy.array([0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1])

# From the sklearn module we will use the LogisticRegression() method to 
# create a logistic regression object.
logr = linear_model.LogisticRegression()
# This object has a method called fit() that takes the independent and 
# dependent values as parameters and fills the regression object with data 
# that describes the relationship:
logr.fit(X,y)


# Now we have a logistic regression object that is ready to whether a tumor 
# is cancerous based on the tumor size:
predicted = logr.predict(numpy.array([3.46]).reshape(-1,1))
str_var = f"Prediction for cancer for size 3.46cm tumor: {predicted}"
print(str_var)

# ======================================================================= <<<<<


# ======================================================================= >>>>>
#	Logistic Regression (Coefficient)
# ======================================================================= >>>>>

# In logistic regression the coefficient is the expected change in log-odds 
# of having the outcome per unit change in X.

# This does not have the most intuitive understanding so let's use it to create 
# something that makes more sense, odds.

log_odds = logr.coef_
odds = numpy.exp(log_odds)
str_var = f"The coeff. is: {log_odds[0]}"
print(str_var)
str_var = f"The odds rate is: {odds[0]} = exp( {log_odds[0]} )"
print(str_var)
# An odd rate of 4.03557295 tells us that as the size of a tumor increases by 1mm 
# the odds of it being a cancerous tumor increases by 4x.

# You can also obtain the intercept of the equation generating the odds.
log_interc = logr.intercept_
str_var = f"The interc. is: {log_interc}"
print(str_var)

# ======================================================================= <<<<<


# ======================================================================= >>>>>
#	Logistic Regression (Probability)
# ======================================================================= >>>>>

# The coefficient and intercept values can be used to find the probability 
# that each tumor is cancerous.
# Create a function that uses the model's coefficient and intercept values to 
# return a new value. This new value represents probability that the given 
# observation is a tumor:
def logit2prob( logr, x ):
  log_odds = logr.coef_ * x + logr.intercept_
  odds = numpy.exp( log_odds )
  probability = odds / ( 1 + odds )
  return( probability )

str_var = "The logarithmetic (natural base) odds is calculated as (X is the tumor size in our example):"
print( str_var )
str_var = "\tlog_odds = coeff. * X + interc."
print( str_var )

str_var = "The odds is calculated as: "
print( str_var )
str_var = "\todds = exp( log_odds )"
print( str_var )

str_var = "The probability (0 = 0%, 1 = 100%) is calculated as: "
print( str_var )
str_var = "\tprob. = odds / ( 1 + odds )"
print( str_var )


print()

# Compute percentage change for cancerous tumor.
perc_prob = logit2prob(logr, X)
# Compute the predict outcome for all initial X set items.
pred_ans = logr.predict(X)

for z in range(len(X)):
    str_var = f"The prob. that {X[z]}cm tumor is cancerous: {perc_prob[z]}"
    print(str_var, end = '. ')
    str_var = f"Predict: {pred_ans[z]}."
    print(str_var)

'''
3.78 0.61 The probability that a tumor with the size 3.78cm is cancerous is 61%.
2.44 0.19 The probability that a tumor with the size 2.44cm is cancerous is 19%.
2.09 0.13 The probability that a tumor with the size 2.09cm is cancerous is 13%.
'''
# ======================================================================= <<<<<


