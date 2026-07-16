



import os, sys
# Make sure the directory above this current one is visible. This is to
# provide access to some local libraries.
currentdir = os.path.dirname(__file__)
src = '../'
sys.path.append( os.path.abspath(os.path.join(currentdir, src)) )


import math
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt


from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential

from toolbox.indexingUtils import rand_samp


# ======================================================================= >>>>>
#       Import Data
# ======================================================================= >>>>>

# Define the data save path and name.
load_dir = currentdir + '/data/norm_plot_data'
load_lin_filestem = 'lin_drop_data'
load_fileext = '.npz'

# Define the full file names for loading the data.
load_lin_FFN = load_dir + '/' + load_lin_filestem + load_fileext

# Load the linear drop data from the designated data directory.
data_tmp = np.load( load_lin_FFN )
x_arr = data_tmp["X"]
y_lin = data_tmp["Y"]
labels_plotType = data_tmp["labels_plotType"]
labels_dropPts = data_tmp["labels_dropPts"]

# ======================================================================= <<<<<


# ======================================================================= >>>>>
#       Data Partitioning
# ======================================================================= >>>>>

# The ratio (out of 1) of data to be assigned as training set (remaining goes to 
# testing).
tr_ratio = 0.6

y_lin_cnt = len( y_lin )        # Total linear set data count.

# Linear data set partition indexing generation.
lin_tr_len = math.floor( y_lin_cnt*tr_ratio )
lin_ts_len = y_lin_cnt - lin_tr_len
lin_tr_idx, lin_ts_idx = rand_samp( y_lin_cnt, lin_tr_len )

# Training and testing sets creation (linear drop).
y_lin_tr = y_lin[ lin_tr_idx ]
y_lin_ts = y_lin[ lin_ts_idx ]
labels_lin_tr = labels_dropPts[ lin_tr_idx ]
labels_lin_ts = labels_dropPts[ lin_ts_idx ]

# ======================================================================= <<<<<


# ======================================================================= >>>>>
#       Model Generation and Testing (Lin Drop Identification)
# ======================================================================= >>>>>

# ------------------------------------------------------------------ >>>>>
#       Model Data Prep
# ------------------------------------------------------------------ >>>>>

load_from_save = True
save_dir = currentdir + '/ML_model_deposit'
model_fullfilename = save_dir + '/script_lin_pts_id_data_train.keras'

# Create a complete set of linear and logistic plot data for training.
X_tr = y_lin_tr
y_tr = labels_lin_tr
# shuffle
idx = np.random.permutation( len( X_tr ) )
X_tr, y_tr = X_tr[idx], y_tr[idx]
# add channel dimension (Initalize at one for greyscale).
X_tr = X_tr[ ..., np.newaxis ]   # (N, L, 1)

# ------------------------------------------------------------------ <<<<<


# ------------------------------------------------------------------ >>>>>
#       Model Training
# ------------------------------------------------------------------ >>>>>

if load_from_save:

    model = keras.models.load_model( model_fullfilename )

else:

    # --- simple 1D CNN classifier ---
    L = X_tr.shape[1]  # Number of data points in each training case.
    inputs = keras.Input( shape=(L, 1) )

    x = layers.Conv1D(32, 5, activation="relu", padding="same")(inputs)
    x = layers.MaxPooling1D(2)(x)
    x = layers.Conv1D(64, 5, activation="relu", padding="same")(x)
    x = layers.GlobalAveragePooling1D()(x)
    x = layers.Dense(64, activation="relu")(x)
    outputs = layers.Dense(2, activation="sigmoid")(x)   # two keypoints

    model = keras.Model(inputs, outputs)
    model.compile(optimizer="adam", loss="mse")

    model.fit(X_tr, y_tr, batch_size=32, epochs=50, validation_split=0.2)

    model.save( model_fullfilename )

# ------------------------------------------------------------------ <<<<<


# ------------------------------------------------------------------ >>>>>
#       Model Testing
# ------------------------------------------------------------------ >>>>>

# Create a complete set of linear and logistic plot data for testing.
X_ts = y_lin_ts
y_ts = labels_lin_ts

# add channel dimension (Initalize at one for grayscale).
X_ts = X_ts[ ..., np.newaxis ]   # (N, L, 1)

test_loss = model.evaluate( X_ts, y_ts )
print( f'Extra test loss: {test_loss:.7f}' )

y_ts_pred = model.predict( X_ts )
y_ts_diff = np.abs( y_ts_pred - y_ts )
y_ts_diff_mean = np.mean( y_ts_diff, axis=-1 )


# print( y_ts_diff_mean.shape )

#  # Print the data and check for error.
# plt.plot( range( lin_ts_len ), y_ts_diff_mean )
# plt.xlabel("x")
# plt.ylabel("y")
# plt.title("Pt wise rms")
# plt.grid(True)
# plt.show()


print( y_ts_pred.shape )
plt.plot( range( lin_ts_len ), y_ts_diff[:,0], label="Y0 diff" )
plt.plot( range( lin_ts_len ), y_ts_diff[:,1], label="Y1 diff" )
plt.xlabel("x")
plt.ylabel("y")
plt.legend()
plt.title("Pt wise diff")
plt.grid(True)
plt.show()

# print( y_ts_pred.shape )
# plt.plot( range( lin_ts_len ), y_ts_pred[:,0] )
# plt.plot( range( lin_ts_len ), y_ts[:,0] )
# plt.xlabel("x")
# plt.ylabel("y")
# plt.title("Y0 predicted vs true")
# plt.grid(True)
# plt.show()

# print( y_ts_pred.shape )
# plt.plot( range( lin_ts_len ), y_ts_pred[:,1] )
# plt.plot( range( lin_ts_len ), y_ts[:,1] )
# plt.xlabel("x")
# plt.ylabel("y")
# plt.title("Y1 predicted vs true")
# plt.grid(True)
# plt.show()


# ------------------------------------------------------------------ <<<<<

# ======================================================================= <<<<<