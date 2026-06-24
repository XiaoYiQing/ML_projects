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
from toolbox.dataUtils import load_png_as_gs_wt_num_labels
from toolbox.dataUtils import get_mnist_tr_ts_sets


# ======================================================================= >>>>>
#       load_png_files_as_gs test
# ======================================================================= >>>>>

# # Define image file source directory.
# img_dir = currentdir + '/char_img_data/additional_0_to_9_digits'

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

# print( Y )

# ======================================================================= <<<<<


# ======================================================================= >>>>>
#       load_png_as_gs_wt_num_labels test
# ======================================================================= >>>>>

# Define image file source directory.
img_dir = currentdir + '/char_img_data/additional_0_to_9_digits'

# The matching image size to the mnist set.
twoDSizes = [ 28, 28 ]

# Obtain the extra test data from the target directory.
X_ts_set2, y_ts_set2 = load_png_as_gs_wt_num_labels( img_dir, twoDSizes )



digit_cnts = np.zeros( len( X_ts_set2 ) ) 
save_dir = currentdir + '/char_img_data/tmp'

for z in range( len( X_ts_set2 ) ):

    # Obtain current image and its label.
    image_z = X_ts_set2[z]
    label_z = y_ts_set2[z]

    img2d_z = image_z.squeeze()             # 28, 28
    img_uint8_z = img2d_z.astype('uint8')

    # Increment the count of the target number.
    digit_cnts[label_z] += 1

    # Set the name of the figure file to be saved.
    img_z_filename = str( label_z ) + '_n' + str( int( digit_cnts[ label_z ] ) ) + '.png'

    # Specify the full path where the image will be saved
    file_path_z = os.path.join( save_dir, img_z_filename )

    # Convert the image to PIL format
    img_z = Image.fromarray( img_uint8_z )

    # Save the image
    img_z.save( file_path_z )


# ======================================================================= <<<<<



# ======================================================================= >>>>>
#       get_mnist_tr_ts_sets test
# ======================================================================= >>>>>

# X_tr, X_ts = get_mnist_tr_ts_sets( 200 )

# print( 'Train set label count: ', len( X_tr ), '.  Test set label count: ', len( X_ts ) )

# for z in range(10):
#     print( z, ' train set shape: ', X_tr[z].shape, ', test set shape: ', X_ts[z].shape )

# ======================================================================= <<<<<
