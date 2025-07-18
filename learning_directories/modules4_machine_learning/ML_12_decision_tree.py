



'''
In this chapter we will show you how to make a "Decision Tree". 
A Decision Tree is a Flow Chart, and can help you make decisions based 
on previous experience.

In the example, a person will try to decide if he/she should go to a 
comedy show or not.

Luckily our example person has registered every time there was a comedy 
show in town, and registered some information about the comedian, and also 
registered if he/she went or not.
'''



# ======================================================================= >>>>>
#	Decision Tree
# ======================================================================= >>>>>

import sys
import os
import pandas

# Define the full file name of the target data file.
dirname = os.path.dirname(__file__)
dataFile_baseName = "ML_12_test_data"
dataFile_fullName = f"{dirname}\\test_data\\{dataFile_baseName}.csv"

df = pandas.read_csv( dataFile_fullName )
# print(df)

# To make a decision tree, all data has to be numerical.
# We have to convert the non numerical columns 'Nationality' and 'Go' into numerical values.
# Pandas has a map() method that takes a dictionary with information on how to convert the values.
d = {'UK': 0, 'USA': 1, 'N': 2}
df['Nationality'] = df['Nationality'].map(d)
d = {'YES': 1, 'NO': 0}
df['Go'] = df['Go'].map(d)
# print(df)


# Then we have to separate the feature columns from the target column.
# 	The feature columns are the columns that we try to predict from.
# 	The target column is the column with the values we try to predict.
features = ['Age', 'Experience', 'Rank', 'Nationality']
X = df[features]
y = df['Go']

print(X)
# print(y)

# ======================================================================= <<<<<



# ======================================================================= >>>>>
#	Decision Tree Formulation
# ======================================================================= >>>>>

from sklearn import tree
from sklearn.tree import DecisionTreeClassifier

import matplotlib.pyplot as plt

dtree = DecisionTreeClassifier()
dtree = dtree.fit(X.values, y.values)

tree.plot_tree(dtree, feature_names=features)

#Two  lines to make our compiler able to draw:
plt.show()

'''
Rank <= 6.5 means that every comedian with a rank of 6.5 or 
lower will follow the True arrow (to the left), and the rest 
will follow the False arrow (to the right).

gini = 0.497 refers to the quality of the split, and is always 
a number between 0.0 and 0.5, where 0.0 would mean all of the samples 
got the same result, and 0.5 would mean that the split is done exactly 
in the middle.

samples = 13 means that there are 13 comedians left at this point in the decision, 
which is all of them since this is the first step.

value = [6, 7] means that of these 13 comedians, 6 will get a "NO", 
and 7 will get a "GO".
'''


'''
Gini
There are many ways to split the samples, we use the GINI method in 
this tutorial.

The Gini method uses this formula:

Gini = 1 - (x/n)^2 - (y/n)^2

Where x is the number of positive answers("GO"), n is the number of samples, 
and y is the number of negative answers ("NO"), which gives us this calculation:

1 - (7 / 13)^2 - (6 / 13)^2 = 0.497
'''
# ======================================================================= <<<<<

str_var = "Should I go see a show starring a 40 years old American "
str_var = str_var + "comedian, with 10 years of experience, and a comedy ranking of 7?"
print(str_var)
pred_ans = dtree.predict( [[40, 10, 7, 1]] )
print( bool( pred_ans.item() ) )
print( pred_ans.__class__ )

str_var = "What is the rank was 6?"
print(str_var)
pred_ans = dtree.predict([[40, 10, 6, 1]])
print( bool( pred_ans.item() ) )
