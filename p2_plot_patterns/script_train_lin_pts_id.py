



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
tr_ratio = 0.4

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


# ======================================================================= <<<<<