'''
This script performs the full run of training a neural network in determining
if an image represents one of the 10 digits from 0 to 9.
'''



import os, sys
# Make sure the directory above this current one is visible. This is to
# provide access to some local libraries.
currentdir = os.path.dirname(__file__)
src = '../'
sys.path.append( os.path.abspath(os.path.join(currentdir, src)) )


import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense


from toolbox import indexingUtils as idxUtils
from toolbox.dataUtils import load_png_files_as_gs
from toolbox.dataUtils import get_mnist_tr_ts_sets






# ======================================================================= >>>>>
#       get_mnist_tr_ts_sets test
# ======================================================================= >>>>>

X_tr, X_ts = get_mnist_tr_ts_sets( 1000 )

# print( 'Train set label count: ', len( X_tr ), '.  Test set label count: ', len( X_ts ) )

# for z in range(10):
#     print( z, ' train set shape: ', X_tr[z].shape, ', test set shape: ', X_ts[z].shape )

# ======================================================================= <<<<<


# ======================================================================= >>>>>
#       Data normalization
# ======================================================================= >>>>>

for label_z in X_tr:
    print( X_tr[ label_z ][0] )
    X_tr[ label_z ] = X_tr[ label_z ]/255.0
    X_ts[ label_z ] = X_ts[ label_z ]/255.0
    print( X_tr[ label_z ][0] )


# ======================================================================= <<<<<
