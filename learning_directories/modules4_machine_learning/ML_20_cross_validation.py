


'''
When adjusting models we are aiming to increase overall model 
performance on unseen data. Hyperparameter tuning can lead to 
much better performance on test sets. However, optimizing 
parameters to the test set can lead information leakage causing 
the model to perform worse on unseen data. To correct this 
we can perform cross validation.

To better understand CV, we will be performing different methods 
on the iris dataset. 
'''

# ======================================================================= >>>>>
#	Cross-Validation: K-Fold
# ======================================================================= >>>>>

from sklearn import datasets
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import KFold, cross_val_score

# Load in and seperate the data.
X, y = datasets.load_iris( return_X_y = True )


'''
There are many methods to cross validation, we will start by looking 
at k-fold cross validation.

k-fold:
The training data used in the model is split into k number of smaller 
sets. 
The model is then trained on k - 1 folds of training set. 
The remaining fold is then used as a validation set to evaluate the model.
This process is repeated until every one of the k folds had a pass as
the validation set exactly once.
Performance metrics from each fold are averaged to estimate the model's 
generalization performance.

As we will be trying to classify different species of iris flowers we 
will need to import a classifier model, for this exercise we will be 
using a DecisionTreeClassifier. We will also need to import CV modules 
from sklearn.
'''

# With the data loaded we can now create and fit a model for evaluation.
clf = DecisionTreeClassifier(random_state=42)

# Now let's evaluate our model and see how it performs on each k-fold.
k_folds = KFold(n_splits = 5)


scores = cross_val_score(clf, X, y, cv = k_folds)
#NOTE: scores is an array the size equal to the number of splits. 
#   Each score is the score of one of the splits.


#print("Cross Validation Scores: ", scores)
print("Average CV Score: ", scores.mean())
print("Number of CV Scores used in Average: ", len(scores))
# ======================================================================= <<<<<


# ======================================================================= >>>>>
#	Cross-Validation: Stratified K-Fold
# ======================================================================= >>>>>

'''
In cases where classes are imbalanced we need a way to account for the
imbalance in both the train and validation sets. To do so we can 
stratify the target classes, meaning that both sets will have an 
equal proportion of all classes.
'''

from sklearn.model_selection import StratifiedKFold

sk_folds = StratifiedKFold(n_splits = 5)

scores = cross_val_score(clf, X, y, cv = sk_folds)

#print("Cross Validation Scores: ", scores)
print("Average CV Score: ", scores.mean())
print("Number of CV Scores used in Average: ", len(scores))

# While the number of folds is the same, the average CV increases 
# from the basic k-fold when making sure there is stratified classes.
# ======================================================================= <<<<<


# ======================================================================= >>>>>
#	Cross-Validation: Leave-One-Out (LOO)
# ======================================================================= >>>>>

'''
LOO is the extreme case of K-Fold when k = n, where n is the total 
number of samples.
This means that a single sample is used as the test 'set' while ALL 
remaining samples are used for training.
As was the case for K-Fold, this process is repeated until every sample
has acted as the test sample exactly once.

Evidently, this is an exhaustive method.
'''

from sklearn.model_selection import LeaveOneOut

loo = LeaveOneOut()

scores = cross_val_score(clf, X, y, cv = loo)

# print("Cross Validation Scores: ", scores)
print("Average CV Score: ", scores.mean())
print("Number of CV Scores used in Average: ", len(scores))

# ======================================================================= <<<<<


# ======================================================================= >>>>>
#	Cross-Validation: Leave-P-Out (LPO)
# ======================================================================= >>>>>

'''
Leave-P-Out is simply a nuanced diffence to the Leave-One-Out idea, 
in that we can select the number of p to use in our validation set.
'''

from sklearn.model_selection import LeavePOut

lpo = LeavePOut(p=2)

scores = cross_val_score(clf, X, y, cv = lpo)

# print("Cross Validation Scores: ", scores)
print("Average CV Score: ", scores.mean())
print("Number of CV Scores used in Average: ", len(scores))

# Notice the huge number of cross-checks since every pairing permutation
# is used for the process.

# ======================================================================= <<<<<


# ======================================================================= >>>>>
#	Cross-Validation: Shuffle Split
# ======================================================================= >>>>>

'''
Unlike KFold, ShuffleSplit reserves a percentage of the data that is not 
used in the train or validation sets. 
To do so we must decide what the train and test sizes are, 
as well as the number of splits.
The shuffle is repeated a number of times that you specify 
(or left as default), where each iteration applies a new random selection
following the same size specification of the train, test, and ignore sets.
This does mean certain data points may participate in more than 1 shuffle.

This option is useful when the data set is simply too large and you are 
not obligated to test/train using the full data set.
'''

from sklearn.model_selection import ShuffleSplit

ss = ShuffleSplit(train_size=0.6, test_size=0.3, n_splits = 5)

scores = cross_val_score(clf, X, y, cv = ss)

# print("Cross Validation Scores: ", scores)
print("Average CV Score: ", scores.mean())
print("Number of CV Scores used in Average: ", len(scores))

# ======================================================================= <<<<<



'''
These are just a few of the CV methods that can be applied to models. 
There are many more cross validation classes, with most models having 
their own class. Check out sklearns cross validation for more CV options.
'''