'''
Starting script where I regain my bearings on how to use everything.

Really just to see if the required libraries are present.

Also, just a place I put temporary tests on the fly.
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
import tensorflow as tf

from PIL import Image
from tensorflow.keras.models import Sequential

# Obtain the database mnist.It contains a training set of 60,000 images and a 
# test set of 10,000 images, each representing digits from 0 to 9.
from keras.datasets import mnist


from toolbox import indexingUtils as idxUtils
from toolbox.dataUtils import zscore_normalize_features
from toolbox.dataUtils import minmax_normalize_features
from toolbox.dataUtils import load_png_files_as_gs
from toolbox.dataUtils import get_mnist_tr_ts_sets


# ======================================================================= >>>>>
#       load_png_files_as_gs test
# ======================================================================= >>>>>

# # Define the directory in which the mnist figures are to be saved.
# img_dir = currentdir + '/char_img_data/mnist'

# twoDSizes = [ 28, 28 ]

# img_arr, Y = load_png_files_as_gs( img_dir, twoDSizes )

# img_arr_shape = img_arr.shape

# img_cnt = img_arr_shape[0]
# img_h = img_arr_shape[1]
# img_w = img_arr_shape[2]
# # For greyscale, its 1 channel only. For RGB, its 3. There are others configs too.
# img_channels_cnt = img_arr_shape[3]


# print( img_cnt )
# print( img_h )
# print( img_w )
# print( img_channels_cnt )

# img_z = img_arr[0]

# ======================================================================= <<<<<


# ======================================================================= >>>>>
#       get_mnist_tr_ts_sets test
# ======================================================================= >>>>>

X_tr, X_ts = get_mnist_tr_ts_sets( 200 )

print( 'Train set label count: ', len( X_tr ), '.  Test set label count: ', len( X_ts ) )

for z in range(10):
    print( z, ' train set shape: ', X_tr[z].shape, ', test set shape: ', X_ts[z].shape )

# ======================================================================= <<<<<
