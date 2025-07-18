

import numpy as np
from sklearn import linear_model

# Tumor size in cm
X1 = np.array([0.14, 1.65, 1.72, 2.09, 2.44, 3.69, 3.78, 4.37, 4.52, 4.92, 4.96, 5.88])
# Tumor age in months
X2 = np.array([1, 1, 2, 2, 2, 3, 2, 4, 3, 5, 4, 5])

X = np.stack( ( X1, X2 ), axis=0 )
# X = np.reshape( X, (-1,2) )
# X = np.flip(X, 1)
X = np.transpose(X)

# Note: X has to be reshaped into a column from a row for the LogisticRegression() 
# function to work.
#X = X.reshape(-1,1)

# y represents whether or not the tumor is cancerous (0 for "No", 1 for "Yes").
y = np.array([0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 2])

print( X.shape )
print( y.shape )

# From the sklearn module we will use the LogisticRegression() method to 
# create a logistic regression object.
logr = linear_model.LogisticRegression()
# This object has a method called fit() that takes the independent and 
# dependent values as parameters and fills the regression object with data 
# that describes the relationship:
logr.fit(X,y)


prediction = np.array([[1.2,1],[2.6,5]])
#prediction = prediction.reshape(1,-1)
# Now we have a logistic regression object that is ready to whether a tumor 
# is cancerous based on the tumor size:
predicted = logr.predict( prediction )
str_var = f"Prediction for cancer for size {prediction}cm tumor: {predicted}"
print(str_var)


