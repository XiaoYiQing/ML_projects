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
import time

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense


from toolbox import indexingUtils as idxUtils
from toolbox.dataUtils import load_png_files_as_gs
from toolbox.dataUtils import get_mnist_tr_ts_sets

from toolbox.indexingUtils import rand_samp



# ======================================================================= >>>>>
#       get_mnist_tr_ts_sets test
# ======================================================================= >>>>>

# The number of training images for each digit.
indiv_tr_set_cnt = 3000

X_tr_arr, X_ts_arr = get_mnist_tr_ts_sets( indiv_tr_set_cnt )

img_shape = X_tr_arr[0][0].shape
img_h = img_shape[0]
img_w = img_shape[1]
channel_cnt = img_shape[2]

# print( 'Train set label count: ', len( X_tr_arr ), '.  Test set label count: ', len( X_ts_arr ) )

# for z in range(10):
#     print( z, ' train set shape: ', X_tr_arr[z].shape, ', test set shape: ', X_ts_arr[z].shape )

# ======================================================================= <<<<<


# ======================================================================= >>>>>
#       Data normalization
# ======================================================================= >>>>>

tr_set_size = 0
ts_set_size = 0

for label_z in X_tr_arr:

    X_tr_arr[ label_z ] = X_tr_arr[ label_z ].astype('float32') /255.0
    X_ts_arr[ label_z ] = X_ts_arr[ label_z ].astype('float32') /255.0

    tr_set_size += len( X_tr_arr[ label_z ] )
    ts_set_size += len( X_ts_arr[ label_z ] )

# ======================================================================= <<<<<



# ======================================================================= >>>>>
#       Sets Assembly
# ======================================================================= >>>>>
'''
Assemble the individual digit data sets into two total data sets (For training
and testing).
'''

X_tr_set = np.zeros( ( 0, img_h, img_w, channel_cnt ) )
X_ts_set = np.zeros( ( 0, img_h, img_w, channel_cnt ) )

y_tr_set = np.zeros( 0 )
y_ts_set = np.zeros( 0 )

for label_z in X_tr_arr:
    
    X_tr_set = np.concatenate( ( X_tr_set, X_tr_arr[label_z] ), axis = 0 )
    X_ts_set = np.concatenate( ( X_ts_set, X_ts_arr[label_z] ), axis = 0 )

    label_z_tr_img_cnt = len( X_tr_arr[label_z] )
    y_tr_set = np.concatenate( ( y_tr_set, label_z * np.ones( label_z_tr_img_cnt ) ), axis = 0 )
    label_z_ts_img_cnt = len( X_ts_arr[label_z] )
    y_ts_set = np.concatenate( ( y_ts_set, label_z * np.ones( label_z_ts_img_cnt ) ), axis = 0 )

# Generate a subset sampling set.
samp_idx, rem_idx = rand_samp( len( X_tr_set ), len( X_tr_set ) )

print( samp_idx.shape )
print( rem_idx.shape )
print( samp_idx[ range(20) ] )

# ======================================================================= <<<<<



# # ======================================================================= >>>>>
# #       Neural Network Training
# # ======================================================================= >>>>>

# model = Sequential([
#     Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=(28, 28, 1)),
#     MaxPooling2D(pool_size=(2, 2)),
#     Conv2D(64, kernel_size=(3, 3), activation='relu'),
#     MaxPooling2D(pool_size=(2, 2)),
#     Flatten(),
#     Dense(128, activation='relu'),
#     Dense(10, activation='softmax')  # 10 classes for digits 0-9
# ])

# model.compile(optimizer='adam',
#     loss='sparse_categorical_crossentropy',
#     metrics=['accuracy'])

# model.fit( X_tr_set, y_tr_set, epochs=10, batch_size=32, validation_split=0.2)


# time.sleep(5)

# # test_loss, test_accuracy = model.evaluate( X_ts_set, y_ts_set )
# test_loss, test_accuracy = model.evaluate( X_tr_set, y_tr_set )
# print(f'Test accuracy: {test_accuracy:.4f}')

# # ======================================================================= <<<<<
