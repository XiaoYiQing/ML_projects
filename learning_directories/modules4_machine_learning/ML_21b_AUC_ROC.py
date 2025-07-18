



# ======================================================================= >>>>>
#	Probabilities
# ======================================================================= >>>>>

import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score, \
    confusion_matrix, roc_auc_score, roc_curve

def plot_roc_curve(true_y, y_prob):
    """
    plots the roc curve based of the probabilities
    """

    fpr, tpr, thresholds = roc_curve(true_y, y_prob)
    plt.plot(fpr, tpr)
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')

'''
Because AUC is a metric that utilizes probabilities of the class 
predictions, we can be more confident in a model that has a higher 
AUC score than one with a lower score even if they have similar 
accuracies.

In the data below, we have two sets of probabilites from hypothetical 
models. The first has probabilities that are not as "confident" 
when predicting the two classes (the probabilities are close to .5). 
The second has probabilities that are more "confident" when predicting
the two classes (the probabilities are close to the extremes of 0 or 1).
'''

n = 10000
y = np.array( [0] * n + [1] * n )
#
y_prob_1 = np.array(
    np.random.uniform(.25, .5, n//2).tolist() +
    np.random.uniform(.3, .7, n).tolist() +
    np.random.uniform(.5, .75, n//2).tolist()
)
y_prob_2 = np.array(
    np.random.uniform(0, .4, n//2).tolist() +
    np.random.uniform(.3, .7, n).tolist() +
    np.random.uniform(.6, 1, n//2).tolist()
)

print(f'model 1 accuracy score: {accuracy_score(y, y_prob_1>.5)}')
print(f'model 2 accuracy score: {accuracy_score(y, y_prob_2>.5)}')

print(f'model 1 AUC score: {roc_auc_score(y, y_prob_1)}')
print(f'model 2 AUC score: {roc_auc_score(y, y_prob_2)}')

plt.figure(1)
plot_roc_curve(y, y_prob_1)
plt.title( "Model I" )
plt.show(block = False)

plt.figure(2)
plot_roc_curve(y, y_prob_2)
plt.title( "Model II" )
plt.show(block = True)


'''
Even though the accuracies for the two models are similar, the 
model with the higher AUC score will be more reliable because it 
takes into account the predicted probability. It is more likely 
to give you higher accuracy when predicting future data.
'''


# ======================================================================= <<<<<





