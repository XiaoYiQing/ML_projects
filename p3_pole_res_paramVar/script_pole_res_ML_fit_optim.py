



import os, sys
# Make sure the directory above this current one is visible. This is to
# provide access to some local libraries.
currentdir = os.path.dirname(__file__)
src = '../'
sys.path.append( os.path.abspath(os.path.join(currentdir, src)) )



import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import random

from tensorflow import keras
from tensorflow.keras import layers
from sklearn.model_selection import train_test_split

from func_depo import PoleResSyst_SISO
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 (needed for 3D)
from toolbox.dataUtils import convert_cconj_to_ReIm_format
from toolbox.dataUtils import convert_ReIm_to_cconj_format
from toolbox.dataUtils import random_in_range
from toolbox.dataUtils import random_re_poly_roots



