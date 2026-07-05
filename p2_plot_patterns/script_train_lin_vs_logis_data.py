


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
load_logis_filestem = 'logistic_drop_data'
load_fileext = '.npz'

# Define the full file names for loading the data.
load_lin_FFN = load_dir + '/' + load_lin_filestem + load_fileext
load_logis_FFN = load_dir + '/' + load_logis_filestem + load_fileext


# Load the linear drop data from the designated data directory.
data_tmp = np.load( load_lin_FFN )
y_lin = data_tmp["Y"]
labels_lin = data_tmp["labels_plotType"]

# Load the logistic drop data from the designated data directory.
data_tmp = np.load( load_logis_FFN )
y_logis = data_tmp["Y"]
labels_logis = data_tmp["labels_plotType"]

# ======================================================================= <<<<<



# ======================================================================= >>>>>
#       Data Partitioning
# ======================================================================= >>>>>

# The ratio (out of 1) of data to be assigned as training set (remaining goes to 
# testing).
tr_ratio = 0.4

y_lin_cnt = len( y_lin )        # Total linear set data count.
y_logis_cnt = len( y_logis )    # Total logistic set data count.

# Linear data set partition indexing generation.
lin_tr_len = math.floor( y_lin_cnt*tr_ratio )
lin_ts_len = y_lin_cnt - lin_tr_len
lin_tr_idx, lin_ts_idx = rand_samp( y_lin_cnt, lin_tr_len )
# Logistic data set partition indexing generation.
logis_tr_len = math.floor( y_logis_cnt*tr_ratio )
logis_ts_len = y_logis_cnt - logis_tr_len
logis_tr_idx, logis_ts_idx = rand_samp( y_logis_cnt, logis_tr_len )

# Training and testing sets creation.
y_lin_tr = y_lin[ lin_tr_idx ]
y_lin_ts = y_lin[ lin_ts_idx ]
labels_lin_tr = labels_lin[ lin_tr_idx ]
labels_lin_ts = labels_lin[ lin_ts_idx ]
y_logis_tr = y_logis[ logis_tr_idx ]
y_logis_ts = y_logis[ logis_ts_idx ]
labels_logis_tr = labels_logis[ logis_tr_idx ]
labels_logis_ts = labels_logis[ logis_ts_idx ]

# ======================================================================= <<<<<


# ======================================================================= >>>>>
#       Model Generation
# ======================================================================= >>>>>

load_from_save = False
save_dir = currentdir + '/ML_model_deposit'
model_fullfilename = save_dir + '/script_lin_logis_data_train.keras'

# Create a complete set of linear and logistic plot data for training.
X_tr = np.concatenate( [ y_lin_tr, y_logis_tr ], axis=0 )
y_tr = np.concatenate( [ labels_lin_tr, labels_logis_tr ], axis=0 )
# shuffle
idx = np.random.permutation( len(X_tr) )
X_tr, y_tr = X_tr[idx], y_tr[idx]
# add channel dimension (Initalize at one for greyscale).
X_tr = X_tr[ ..., np.newaxis ]   # (N, L, 1)

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
    x = layers.Dense(32, activation="relu")(x)
    outputs = layers.Dense(1, activation="sigmoid")(x)

    model = keras.Model(inputs, outputs)
    model.compile(optimizer="adam",
                loss="binary_crossentropy",
                metrics=["accuracy"])

    model.fit( X_tr, y_tr, batch_size=32, epochs=20, validation_split=0.2 )

    model.save( model_fullfilename )

# ======================================================================= <<<<<


# ======================================================================= >>>>>
#       Testing Set Test
# ======================================================================= >>>>>

# Create a complete set of linear and logistic plot data for testing.
X_ts = np.concatenate( [ y_lin_ts, y_logis_ts ], axis=0 )
y_ts = np.concatenate( [ labels_lin_ts, labels_logis_ts ], axis=0 )

# add channel dimension (Initalize at one for grayscale).
X_ts = X_ts[ ..., np.newaxis ]   # (N, L, 1)

test_loss, test_accuracy = model.evaluate( X_ts, y_ts )
# test_loss, test_accuracy = model.evaluate( X_tr_set, y_tr_set )
print( f'Extra test accuracy: {test_accuracy:.4f}' )
print( f'Extra test loss: {test_loss:.4f}' )

# ======================================================================= <<<<<