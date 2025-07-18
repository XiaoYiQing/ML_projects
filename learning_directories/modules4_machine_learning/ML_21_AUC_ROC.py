


'''
In classification, there are many different evaluation metrics. 
The most popular is accuracy, which measures how often the model 
is correct. This is a great metric because it is easy to understand 
and getting the most correct guesses is often desired. 
There are some cases where you might consider using another 
evaluation metric.

Another common metric is the area under curve (AUC), which is simply 
the area under the receiver operating characteristic (ROC) curve.
The ROC curve plots the true positive rate (TPR) versus the false positive 
rate (FPR) at different classification thresholds. 
    TPR = TP/(TP + FN) = TP/(total # of positives)
    FPR = FP/(FP + TN) = FP/(total # of negatives)
The thresholds are different probability cutoffs that separate the 
two classes in binary classification. It uses probability to tell 
us how well a model separates the classes.
'''


# ======================================================================= >>>>>
#	Imbalanced Data
# ======================================================================= >>>>>

import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score, \
    confusion_matrix, roc_auc_score, roc_curve


# Suppose we have an imbalanced data set where the majority of our data 
# is of one value. We can obtain high accuracy for the model by predicting 
# the majority class.


# Imprint the ratio 0.95 into the n=10000 scenario. 
n = 10000
ratio = .95
n_0 = int((1-ratio) * n)
n_1 = int(ratio * n)

# Create an array of 0 and 1, where the number of instances of each
# is n_0 and n_1, respectively.
# We refer to the two values as class 0 and class 1.
y = np.array([0] * n_0 + [1] * n_1)

# Create the prediction of a dummy model that always guess class 1.
y_proba = np.array([1]*n)
y_pred = y_proba > .5


acc_score = accuracy_score(y, y_pred)
print(f'accuracy score: {acc_score}')

# Create a confusion matrix.
cf_mat = confusion_matrix(y, y_pred)
print('Confusion matrix')
print(cf_mat)
print(f'class 0 accuracy: {cf_mat[0][0]/n_0}')
print(f'class 1 accuracy: {cf_mat[1][1]/n_1}')

'''
TN = C_{0,0}
FN = C_{1,0} 
TP = C_{1,1}
FP = C_{0,1}

    C_{1,1}     C_{0,1}
    C_{1,0}     C_{0,0}

    TP = 9500   FP = 500
    FN = 0      TN = 0

    TPR = TP/(TP + FN) = 1
    FPR = FP/(FP + TN) = 1

Obviously, class 0 accuracy is 0 since the model only guesses class 1, 
which also implies perfect accuracy in class 1 prediction.
This results in an overall "highly accurate" model since accuracy is 
at 95%, but error is guaranteed on class 0.
'''

# ======================================================================= <<<<<

print() 

# ======================================================================= >>>>>
#	Imbalanced Data (Part 2)
# ======================================================================= >>>>>

# below are the probabilities obtained from a hypothetical model that 
# doesn't always predict the mode
y_proba_2 = np.array(
    np.random.uniform(0, .7, n_0).tolist() +
    np.random.uniform(.3, 1, n_1).tolist()
)
y_pred_2 = y_proba_2 > .5

print(f'accuracy score: {accuracy_score(y, y_pred_2)}')
cf_mat = confusion_matrix(y, y_pred_2)
print('Confusion matrix')
print(cf_mat)
print(f'class 0 accuracy: {cf_mat[0][0]/n_0}')
print(f'class 1 accuracy: {cf_mat[1][1]/n_1}')


TP = cf_mat[1][1]
FP = cf_mat[0][1]
FN = cf_mat[1][0]
TN = cf_mat[0][0]

TRP = TP/(TP + FN)
FPR = FP/(FP + TN)

print("TRP: ", TRP, '\t', "FRP: ", FPR)

'''
For the second set of predictions, we do not have as high of an 
accuracy score as the first, but the accuracy for each class is 
more balanced. Using accuracy as an evaluation metric we would 
rate the first model higher than the second even though it doesn't 
tell us anything about the data.
'''

'''
In cases like this, using another evaluation metric like AUC would 
be preferred.
Let's define a function that would plot the ROC for us:
'''

def plot_roc_curve(true_y, y_prob):
    """
    plots the roc curve based of the probabilities
    """

    fpr, tpr, thresholds = roc_curve(true_y, y_prob)
    plt.plot(fpr, tpr)
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')



plot_roc_curve(y, y_proba)
plt.title( "Model I" )
plt.show(block = False)
print( f'model 1 AUC score: {roc_auc_score(y, y_proba)}' )


plot_roc_curve(y, y_proba_2)
plt.title( "Model II" )
plt.show(block = True)
print(f'model 2 AUC score: {roc_auc_score(y, y_proba_2)}')
# ======================================================================= <<<<<




