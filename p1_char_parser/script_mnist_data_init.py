'''
Script where I initialize the mnist data in a ready to be used format.

Also, I regulate the amount of data to participate in the NN training and
the amount of data to be used for testing.
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

from PIL import Image

# Obtain the database mnist. It contains a training set of 60,000 images and a 
# test set of 10,000 images, each representing digits from 0 to 9.
from keras.datasets import mnist


from toolbox.indexingUtils import rand_samp


# ======================================================================= >>>>>
#       mnist Data Import
# ======================================================================= >>>>>

# Obtain all the 0 to 9 image database.
(X_tr, y_tr), (X_ts, y_ts) = mnist.load_data()

# Obtain the shapes of the training set data.
X_tr_shape = X_tr.shape
y_tr_shape = y_tr.shape
# Obtain the shapes of the testing set data.
X_ts_shape = X_ts.shape
y_ts_shape = y_ts.shape

# Obtain the image dataset properties.
tr_img_cnt = X_tr_shape[0]
ts_img_cnt = X_ts_shape[0]
tot_img_cnt = tr_img_cnt + ts_img_cnt
img_height = X_tr_shape[1]
img_width =  X_tr_shape[2]

# Initialize a dictionary to store images by their label.
digit_arrs_list = { label: [] for label in range(10) }

# Counter of each digit from 0 to 9.
digit_cnts = np.zeros(10) 

# Distribute the training set images based on their label value.
for z in range( tr_img_cnt ):

    label_z = y_tr[z]
    image_z = X_tr[z]
    digit_arrs_list[ label_z ].append( image_z )

    digit_cnts[ label_z ] += 1        # Count the numbers of digit

# Distribute the testing set images based on their label value.
for z in range( ts_img_cnt ):
    
    label_z = y_ts[z]
    image_z = X_ts[z]
    digit_arrs_list[ label_z ].append( image_z )

    digit_cnts[ label_z ] += 1        # Count the numbers of digit

# Convert lists to np arrays and add an extra dimension for the channel if needed
for label_z in digit_arrs_list:

    images_z = digit_arrs_list[label_z]
    # Adding the singular channel dimension and converting lists to np.array
    digit_arrs_list[label_z] = np.array(images_z).reshape(-1, img_height, img_width, 1)


# Obtain the smallest digit batch size amongst the numbers from 0 to 9.
min_digit_cnt = np.min( digit_cnts )

# ======================================================================= <<<<<


# ======================================================================= >>>>>
#       mnist Training and Testing Data Sets Subdivision
# ======================================================================= >>>>>

# Define the number of image samples to retain from each digit's image array.
subset_size = 1500
subset_size = min( subset_size, min_digit_cnt )

# Initialize a dictionary to store training images by their label.
digit_train_list = { label: [] for label in range(10) }
# Initialize a dictionary to store test images by their label.
digit_test_list = { label: [] for label in range(10) }


for label_z in digit_arrs_list:

    # Obtain current digit's image array.
    img_arr_z = digit_arrs_list[label_z]

    # Generate a subset sampling set.
    samp_idx, rem_idx = rand_samp( len( img_arr_z ), subset_size )

    # Subdivide the whole set into the training and sampling sets according the 
    # the given random sampling indexing.
    digit_train_list[label_z] = img_arr_z[ samp_idx ]
    digit_test_list[label_z] = img_arr_z[ rem_idx ]


# ======================================================================= <<<<<