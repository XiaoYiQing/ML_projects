


'''
The majority of machine learning models contain parameters that can be 
adjusted to vary how the model learns. 
For example, the logistic regression model, from sklearn, has a parameter 
C that controls regularization,which affects the complexity of the model.

How do we pick the best value for C? The best value is dependent on the 
data used to train the model.
'''

'''
One method is to try out different values and then pick the value that gives
the best score. This technique is known as a grid search. 
If we had to select the values for two or more parameters, we would evaluate 
all combinations of the sets of values thus forming a grid of values.

Before we get into the example it is good to know what the parameter we are 
changing does. Higher values of C tell the model, the training data resembles 
real world information, place a greater weight on the training data. 
While lower values of C do the opposite.
'''


# ======================================================================= >>>>>
#	Grid Search (Initial Case)
# ======================================================================= >>>>>

import numpy
from sklearn import datasets
from sklearn.linear_model import LogisticRegression


# First, we load a standard template data set.
iris = datasets.load_iris()

# Next in order to create the model we must have a set of independent 
# variables X and a dependant variable y
X = iris['data']
y = iris['target']


# Creating the model, setting max_iter to a higher value to ensure that 
# the model finds a result.
# NOTE: We put C = 1, but it would have been C=1 by default.
logit = LogisticRegression(C = 1, max_iter = 10000)
# After we create the model, we must fit the model to the data.
logit.fit(X,y)
# To evaluate the model we run the score method.
str_var = f"logit fit score (): {logit.score(X,y)}"
print(str_var)

# With the default setting of C = 1, we achieved a score of 0.973.

# ======================================================================= <<<<<


# ======================================================================= >>>>>
#	Grid Search (Implementation)
# ======================================================================= >>>>>

# [0.25, 0.5, 0.75, 1, 1.25, 1.5, 1.75, 2]

# Since the default value for C is 1, we will set a range of 
# values surrounding it.
C_tmp = numpy.linspace(0.25,3.00,6)
C = C_tmp.tolist()


# First we will create an empty list to store the score within.
scores = []

# To change the values of C we must loop over the range of values and 
# update the parameter each time.
for z in range(len(C)):
  logit.set_params( C = C[z] )
  logit.fit(X, y)
  score_z = logit.score(X, y)
  scores.append(score_z)

  txt = f"C={C[z]:.2f} fit has score: {score_z:.6f}"
  print(txt)

# print(scores)

# ======================================================================= <<<<<


'''
Note on Best Practices
We scored our logistic regression model by using the same data that was 
used to train it. If the model corresponds too closely to that data, it 
may not be great at predicting unseen data. 
This statistical error is known as over fitting.

To avoid being misled by the scores on the training data, we can put aside a
portion of our data and use it specifically for the purpose of testing the model. 
Refer to the lecture on train/test splitting to avoid being misled and 
overfitting.
'''

