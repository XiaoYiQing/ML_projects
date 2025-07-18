



'''
What is a confusion matrix?
It is a table that is used in classification problems to assess where 
errors in the model were made.

The rows represent the actual classes the outcomes should have been. 
While the columns represent the predictions we have made. 
Using this table it is easy to see which predictions are wrong.
'''

# ======================================================================= >>>>>
#	Confusion Matrix
# ======================================================================= >>>>>

import numpy
from sklearn import metrics
import matplotlib.pyplot as plt


# Next we will need to generate the numbers for "actual" and "predicted" values.
actual = numpy.random.binomial(1, 0.9, size = 25)
predicted = numpy.random.binomial(1, 0.9, size = 25)
# print(actual)
# print(predicted)

confusion_matrix = metrics.confusion_matrix(actual, predicted)

display_labels = [0, 1]
cm_display = metrics.ConfusionMatrixDisplay(confusion_matrix = confusion_matrix, \
        display_labels = display_labels)

cm_display.plot()
plt.show()

'''
The Confusion Matrix created has four different quadrants:

    True Negative (Top-Left Quadrant)
    False Positive (Top-Right Quadrant)
    False Negative (Bottom-Left Quadrant)
    True Positive (Bottom-Right Quadrant)

True means that the values were accurately predicted, 
False means that there was an error or wrong prediction.

Now that we have made a Confusion Matrix, we can calculate different 
measures to quantify the quality of the model. First, lets look at Accuracy.
'''

# ======================================================================= <<<<<


# ======================================================================= >>>>>
#	Confusion Matrix (Metrics)
# ======================================================================= >>>>>

'''
The matrix provides us with many useful metrics that help us to evaluate 
out classification model.

The different measures include: 
    Accuracy, Precision, Sensitivity (Recall), 
    Specificity, and the F-score, explained below.
'''


# Accuracy measures how often the model is correct.
# Accuracy = (True Positive + True Negative) / Total Predictions
Accuracy = metrics.accuracy_score(actual, predicted)
str_var = f"Accuracy: {Accuracy}"
print(str_var)


# Precision: of the positives predicted, what percentage is truly positive?
# Precision = True Positive / (True Positive + False Positive)
# Precision does not evaluate the correctly predicted negative cases.
Precision = metrics.precision_score(actual, predicted)
str_var = f"Precision: {Precision}"
print(str_var)

# Sensitivity (sometimes called Recall) measures how good the model is at 
#   predicting positives.
# Sensitivity = True Positive / (True Positive + False Negative)
Sensitivity_recall = metrics.recall_score(actual, predicted)
str_var = f"Sensitivity (recall): {Sensitivity_recall}"
print(str_var)


# Specificity is similar to sensitivity, but looks at it from the persepctive 
#   of negative results.
# How good the model is at predicting negatives.
# Specificity = True Negative / (True Negative + False Positive)
# Since it is just the opposite of Recall, we use the recall_score function, 
#   taking the opposite position label:
Specificity = metrics.recall_score(actual, predicted, pos_label=0)
str_var = f"Specificity: {Specificity}"
print(str_var)


# F-score is the "harmonic mean" of precision and sensitivity.
# It considers both false positive and false negative cases and is good for 
#   imbalanced datasets.
# F-score = 2 * ((Precision * Sensitivity) / (Precision + Sensitivity))
F1_score = metrics.f1_score(actual, predicted)
str_var = f"F1 score: {F1_score}"
print(str_var)
# ======================================================================= <<<<<


