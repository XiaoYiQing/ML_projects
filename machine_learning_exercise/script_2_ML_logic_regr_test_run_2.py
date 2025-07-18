
'''
This script runs a Machine Learning (ML) simulation which goal is to build
a model that can differentiate vegetable from protein based food.

The ML algorithm used use the logistic regression algorithm.
'''


import os, sys
# Make sure the directory above this current one is visible.
currentdir = os.path.dirname(__file__)
src = '../'
sys.path.append( os.path.abspath(os.path.join(currentdir, src)) )


import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn import linear_model
from sklearn import metrics

import foodDataParser as fdPar
from machine_learning_exercise.ML_5fdGr import ML_5fdGr_runner
from toolbox import indexingUtils as idxUtils



ML_runner = ML_5fdGr_runner()


ML_res = ML_runner.logRegr_2comp( 1, 2 )


print( ML_res.get_pred_right() )
print( ML_res.get_acc() )
print( ML_res.get_acc_gr1() )
print( ML_res.get_acc_gr2() )

# display_labels = [0, 1]
# cm_display = metrics.ConfusionMatrixDisplay(confusion_matrix = conf_mat_tmp, \
#         display_labels = display_labels)
# cm_display.plot()
# plt.show(block = False)

# ML_res = ML_runner.decTree_2comp( 3, 4 )

# confusion_matrix = gr1_res["conf_mat"]
# display_labels = [0, 1]
# cm_display = metrics.ConfusionMatrixDisplay(confusion_matrix = confusion_matrix, \
#         display_labels = display_labels)
# cm_display.plot()
# plt.show(block = False)

# confusion_matrix = gr2_res["conf_mat"]
# display_labels = [0, 1]
# cm_display = metrics.ConfusionMatrixDisplay(confusion_matrix = confusion_matrix, \
#         display_labels = display_labels)
# cm_display.plot()
# plt.show()


# ML_res = ML_runner.hiera_cluster_2comp( 1, 3 )

# ML_res = ML_runner.K_means_2comp( 1, 3 )

