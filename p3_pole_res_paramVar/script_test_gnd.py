'''
Starting script where I do quick tests of things I'll be working on.
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