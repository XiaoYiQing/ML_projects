


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
load_linPolyLin_filestem = 'linPolyLin_data'
load_fileext = '.npz'

# Define the full file names for loading the data.
load_lin_FFN = load_dir + '/' + load_lin_filestem + load_fileext
load_logis_FFN = load_dir + '/' + load_logis_filestem + load_fileext
load_linPolyLin_FFN = load_dir + '/' + load_linPolyLin_filestem + load_fileext


# Load the linear drop data from the designated data directory.
data_tmp = np.load( load_lin_FFN )
y_lin = data_tmp["Y"]
labels_lin = data_tmp["labels"]

# Load the logistic drop data from the designated data directory.
data_tmp = np.load( load_logis_FFN )
y_logis = data_tmp["Y"]
labels_logis = data_tmp["labels"]

# Load the LinPolyLin drop data from the designated data directory.
data_tmp = np.load( load_linPolyLin_FFN )
y_LPL = data_tmp["Y"]
labels_LPL = data_tmp["labels"]

# ======================================================================= <<<<<